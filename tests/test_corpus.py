"""Corpus, PoC grading and evidence integrity tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pocforge.corpus import BY_SLUG, PACK, SKILLS  # noqa: E402
from pocforge.evidence import (  # noqa: E402
    EvidenceError,
    build_manifest,
    collect,
    infer_root,
    load_manifest,
    sha256_file,
    verify_manifest,
    write_manifest,
)
from pocforge.render import render_skill, word_count  # noqa: E402
from pocforge.spec import (  # noqa: E402
    SCHEMA,
    grade,
    load_spec,
    render_report,
    scaffold,
)
from pocforge.validate import validate_pack  # noqa: E402

EXAMPLE_SPEC = ROOT / "examples" / "poc" / "idor-order-read.json"
EXAMPLE_EVIDENCE = ROOT / "examples" / "evidence"
PNG_BYTES = b"\x89PNG\r\n\x1a\n"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = {"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-m", "pocforge", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=300,
    )


# ---------------------------------------------------------------- corpus shape


def test_pack_declares_fifty_and_delivers_fifty() -> None:
    assert PACK["expected_skills"] == 50
    assert len(SKILLS) == 50


def test_slugs_and_titles_are_unique() -> None:
    assert len({skill.slug for skill in SKILLS}) == 50
    assert len({skill.title.lower() for skill in SKILLS}) == 50


def test_every_skill_passes_the_strict_gate() -> None:
    assert validate_pack(PACK, SKILLS) == []


def test_phases_cover_the_whole_lifecycle() -> None:
    phases = {skill.meta_get("phase") for skill in SKILLS}
    assert phases == {"frame", "reproduce", "minimize", "oracle", "verify", "package"}
    for phase in phases:
        assert len([skill for skill in SKILLS if skill.meta_get("phase") == phase]) >= 8


def test_every_skill_is_substantial_enough_to_use() -> None:
    for skill in SKILLS:
        assert word_count(render_skill(PACK, skill)) >= 180, skill.slug
        assert len(skill.patterns) >= 3, skill.slug


def test_lookup_table_matches_the_corpus() -> None:
    assert set(BY_SLUG) == {skill.slug for skill in SKILLS}


# ------------------------------------------------------------ committed output


def test_committed_skills_match_a_fresh_render() -> None:
    for skill in SKILLS:
        path = ROOT / "skills" / skill.slug / "SKILL.md"
        assert path.is_file(), f"missing {path}"
        assert path.read_text(encoding="utf-8") == render_skill(PACK, skill), skill.slug


def test_pack_json_matches_the_corpus() -> None:
    manifest = json.loads((ROOT / "pack.json").read_text(encoding="utf-8"))
    assert manifest["skill_count"] == 50
    assert [entry["slug"] for entry in manifest["skills"]] == [s.slug for s in SKILLS]
    for entry in manifest["skills"]:
        text = (ROOT / entry["path"]).read_text(encoding="utf-8")
        assert sha256_file(ROOT / entry["path"]) == entry["sha256"]
        assert text.startswith("---\n")


# -------------------------------------------------------------------- grading


def test_example_poc_is_submittable() -> None:
    spec = load_spec(EXAMPLE_SPEC)
    report = grade(spec, evidence_root=EXAMPLE_EVIDENCE)
    assert report.submittable, [f.message for f in report.blocking]
    assert report.grade == "A"
    assert report.score == 100


def test_scaffold_passes_structure_but_fails_scope() -> None:
    report = grade(scaffold("A title that is long enough", "demo"))
    rules = {finding.rule for finding in report.findings}
    assert "scope-ref" in rules
    assert "authorized" in rules
    assert "oracle" not in rules
    assert "negative-control" not in rules
    assert report.submittable is False


def _spec() -> dict:
    return load_spec(EXAMPLE_SPEC)


def test_missing_scope_reference_blocks_submission() -> None:
    spec = _spec()
    spec["target"]["scope_ref"] = ""
    report = grade(spec)
    assert "scope-ref" in {f.rule for f in report.blocking}
    assert report.grade == "D"


def test_oracle_needs_both_sides() -> None:
    spec = _spec()
    spec["oracle"]["failure"] = []
    report = grade(spec)
    assert "oracle" in {f.rule for f in report.blocking}


def test_nondeterministic_oracle_is_a_major_finding() -> None:
    spec = _spec()
    spec["oracle"]["deterministic"] = False
    report = grade(spec)
    finding = next(f for f in report.findings if f.rule == "oracle-determinism")
    assert finding.severity == "major"
    assert report.submittable is True
    assert report.score == 90


def test_control_step_is_required() -> None:
    spec = _spec()
    for step in spec["steps"]:
        step.pop("control", None)
    spec.pop("control", None)
    report = grade(spec)
    assert "negative-control" in {f.rule for f in report.blocking}


def test_mutating_poc_needs_cleanup() -> None:
    spec = _spec()
    spec["cleanup"] = []
    spec["evidence"] = []
    report = grade(spec)
    rules = {f.rule for f in report.blocking}
    assert "cleanup" in rules
    assert "evidence" in rules


def test_evidence_digest_must_be_real_hex() -> None:
    spec = _spec()
    spec["evidence"][0]["sha256"] = "not-a-hash"
    report = grade(spec)
    assert "evidence-digest" in {f.rule for f in report.blocking}


def test_step_without_expectation_blocks() -> None:
    spec = _spec()
    spec["steps"][2]["expect"] = {}
    report = grade(spec)
    assert "step-expect" in {f.rule for f in report.blocking}


def test_tampered_evidence_blocks_the_spec(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / "trigger.http").write_text("HTTP/1.1 200 OK\n", encoding="utf-8")
    manifest = build_manifest(evidence)
    write_manifest(manifest, evidence / "manifest.json")

    spec = json.loads(EXAMPLE_SPEC.read_text(encoding="utf-8"))
    spec["evidence"] = [
        {
            "kind": "http",
            "ref": "trigger.http",
            "bytes": manifest["files"][0]["bytes"],
            "sha256": manifest["files"][0]["sha256"],
        }
    ]
    spec["evidence_manifest"] = "manifest.json"
    assert grade(spec, evidence_root=evidence).submittable

    (evidence / "trigger.http").write_text("HTTP/1.1 403 OK\n", encoding="utf-8")
    report = grade(spec, evidence_root=evidence)
    assert "evidence-verify" in {f.rule for f in report.blocking}
    assert any("digest changed" in f.message for f in report.blocking)


def test_report_renders_the_grade_and_impact() -> None:
    spec = load_spec(EXAMPLE_SPEC)
    text = render_report(spec, grade(spec, evidence_root=EXAMPLE_EVIDENCE))
    assert "## Proof grade" in text
    assert "**A**" in text
    assert "Cross-tenant read of order records" in text
    assert "POC-ALICE-7741" in text


# ------------------------------------------------------------------- evidence


def test_manifest_records_relative_paths_and_digests(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    root.mkdir()
    (root / "a.http").write_text("one", encoding="utf-8")
    (root / "b.png").write_bytes(PNG_BYTES)

    manifest = build_manifest(root)
    assert manifest["schema"] == "pocforge.evidence/v1"
    assert manifest["count"] == 2
    assert [entry["path"] for entry in manifest["files"]] == ["a.http", "b.png"]
    assert manifest["total_bytes"] == 3 + len(PNG_BYTES)
    assert all(len(entry["sha256"]) == 64 for entry in manifest["files"])


def test_manifest_verifies_from_its_own_directory(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    root.mkdir()
    (root / "a.http").write_text("one", encoding="utf-8")
    manifest = build_manifest(root)
    write_manifest(manifest, root / "manifest.json")

    assert verify_manifest(manifest, root, manifest_path=root / "manifest.json") == []


def test_verify_reports_missing_changed_and_unrecorded(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    root.mkdir()
    (root / "keep.http").write_text("one", encoding="utf-8")
    (root / "gone.http").write_text("two", encoding="utf-8")
    manifest = build_manifest(root)

    (root / "gone.http").unlink()
    (root / "keep.http").write_text("one and a half", encoding="utf-8")
    (root / "extra.http").write_text("three", encoding="utf-8")

    problems = verify_manifest(manifest, root)
    assert any(problem.startswith("missing: gone.http") for problem in problems)
    assert any("size changed: keep.http" in problem for problem in problems)
    assert any("unrecorded file: extra.http" in problem for problem in problems)


def test_build_manifest_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(EvidenceError):
        build_manifest(tmp_path, ["nope.http"])


def test_collect_expands_directories(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "x.http").write_text("x", encoding="utf-8")
    (tmp_path / "y.http").write_text("y", encoding="utf-8")

    files = collect(tmp_path, ["nested"])
    assert [path.name for path in files] == ["x.http"]


def test_infer_root_uses_the_common_parent(tmp_path: Path) -> None:
    root = tmp_path / "evidence"
    root.mkdir()
    first = root / "a.http"
    second = root / "b.http"
    first.write_text("a", encoding="utf-8")
    second.write_text("b", encoding="utf-8")
    assert infer_root([first, second]) == root.resolve()


def test_load_manifest_rejects_foreign_schema(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"schema": "other/v9", "files": []}), encoding="utf-8")
    with pytest.raises(EvidenceError):
        load_manifest(path)


# ------------------------------------------------------------------------ cli


def test_cli_validate_check_and_scaffold() -> None:
    result = run_cli("validate", "--json")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] == 50
    assert payload["passed"] is True

    ok = run_cli("check", str(EXAMPLE_SPEC), "--evidence-root", str(EXAMPLE_EVIDENCE))
    assert ok.returncode == 0, ok.stdout
    assert "grade A" in ok.stdout

    bad = run_cli("check", str(EXAMPLE_SPEC))
    assert bad.returncode == 0

    scaffold_path = ROOT / "results" / "_scaffold_probe.json"
    made = run_cli("scaffold", "A probe title for the grader", "--id", "probe", "--out", str(scaffold_path))
    assert made.returncode == 0, made.stderr
    probe = run_cli("check", str(scaffold_path))
    assert probe.returncode == 1
    scaffold_path.unlink()

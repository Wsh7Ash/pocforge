"""PoC specification model, rule engine and grading.

The rule set encodes what a triager actually rejects a report for: no scope
reference, no way to tell success from failure, no negative control, an effect
that was never cleaned up, and evidence nobody can verify. Each rule carries a
severity so a PoC can be graded instead of merely passing or failing.

    spec = load_spec(Path("poc.json"))
    report = grade(spec, evidence_root=Path("results"))
    print(report.grade, report.blocking)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .evidence import EvidenceError, verify_manifest

SCHEMA = "pocforge/v1"

BLOCKING = "blocking"
MAJOR = "major"
MINOR = "minor"
PENALTY = {BLOCKING: 25, MAJOR: 10, MINOR: 3}

MUTATING_METHODS = ("POST", "PUT", "PATCH", "DELETE")
SEVERITIES = ("low", "medium", "high", "critical")
MIN_STEPS = 3
MIN_PRECONDITIONS = 2
MIN_ACTION = 10


class SpecError(RuntimeError):
    """Raised when a PoC spec cannot be read at all."""


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    message: str
    hint: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "hint": self.hint,
        }


@dataclass
class Report:
    spec_id: str
    score: int
    grade: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def blocking(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == BLOCKING]

    @property
    def submittable(self) -> bool:
        return not self.blocking

    def as_dict(self) -> dict[str, Any]:
        return {
            "spec": self.spec_id,
            "score": self.score,
            "grade": self.grade,
            "submittable": self.submittable,
            "counts": {
                BLOCKING: len(self.blocking),
                MAJOR: len([f for f in self.findings if f.severity == MAJOR]),
                MINOR: len([f for f in self.findings if f.severity == MINOR]),
            },
            "findings": [item.as_dict() for item in self.findings],
        }


def load_spec(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SpecError(f"spec not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SpecError(f"spec is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecError("spec must be a JSON object")
    return data


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _steps(spec: dict[str, Any]) -> list[dict[str, Any]]:
    return [step for step in _items(spec.get("steps")) if isinstance(step, dict)]


def _oracle(spec: dict[str, Any]) -> dict[str, Any]:
    oracle = spec.get("oracle")
    return oracle if isinstance(oracle, dict) else {}


def _target(spec: dict[str, Any]) -> dict[str, Any]:
    target = spec.get("target")
    return target if isinstance(target, dict) else {}


def _impact(spec: dict[str, Any]) -> dict[str, Any]:
    impact = spec.get("impact")
    return impact if isinstance(impact, dict) else {}


def _method(step: dict[str, Any]) -> str:
    request = step.get("request")
    if isinstance(request, dict):
        return _text(request.get("method")).upper()
    return _text(step.get("method")).upper()


def grade(spec: dict[str, Any], evidence_root: Path | None = None) -> Report:
    """Run every rule and grade the PoC."""
    findings: list[Finding] = []

    def add(rule: str, severity: str, message: str, hint: str = "") -> None:
        findings.append(Finding(rule, severity, message, hint))

    if _text(spec.get("schema")) != SCHEMA:
        add(
            "schema",
            BLOCKING,
            f"spec schema must be {SCHEMA!r}",
            "Copy the scaffold output; older drafts silently drop required blocks.",
        )

    spec_id = _text(spec.get("id")) or "unnamed"
    if not _text(spec.get("id")):
        add("id", MAJOR, "spec has no stable id", "Use the tracker id so retests map to one spec.")
    if len(_text(spec.get("title"))) < 8:
        add("title", MAJOR, "title is missing or too short to be searchable")

    target = _target(spec)
    if not _text(target.get("scope_ref")):
        add(
            "scope-ref",
            BLOCKING,
            "target has no scope reference",
            "Quote the program scope line the asset appears under.",
        )
    if target.get("authorized") is not True:
        add(
            "authorized",
            BLOCKING,
            "target is not marked authorized",
            "Set authorized only after checking the program's current scope.",
        )

    preconditions = [item for item in _items(spec.get("preconditions")) if _text(item)]
    if len(preconditions) < MIN_PRECONDITIONS:
        add(
            "preconditions",
            MAJOR,
            f"found {len(preconditions)} precondition(s), need {MIN_PRECONDITIONS}",
            "State accounts, roles and starting data the triager must recreate.",
        )

    steps = _steps(spec)
    if len(steps) < MIN_STEPS:
        add(
            "steps",
            BLOCKING,
            f"found {len(steps)} step(s), need {MIN_STEPS}",
            "A PoC needs setup, the trigger and the observation, not just the trigger.",
        )

    numbers = [step.get("n") for step in steps]
    if numbers and numbers != list(range(1, len(steps) + 1)):
        add("step-numbering", MINOR, "steps are not numbered 1..n in order")

    for index, step in enumerate(steps, start=1):
        action = _text(step.get("action"))
        if len(action) < MIN_ACTION:
            add(
                "step-action",
                BLOCKING if not action else MAJOR,
                f"step {index} has no usable action text",
                "Describe what is sent and as which identity.",
            )
        if not step.get("expect"):
            add(
                "step-expect",
                BLOCKING,
                f"step {index} records no expected result",
                "Without an expectation the step cannot fail, so it proves nothing.",
            )

    oracle = _oracle(spec)
    success = [item for item in _items(oracle.get("success")) if _text(item)]
    failure = [item for item in _items(oracle.get("failure")) if _text(item)]
    if not success or not failure:
        add(
            "oracle",
            BLOCKING,
            "oracle must define both success and failure conditions",
            "A differential needs a control response to compare against.",
        )
    if oracle.get("deterministic") is not True:
        add(
            "oracle-determinism",
            MAJOR,
            "oracle is not marked deterministic",
            "Flaky triggers need N-of-M wording or they will be closed as intermittent.",
        )

    control = _text(spec.get("control")) or any(
        step.get("control") is True for step in steps
    )
    if not control:
        add(
            "negative-control",
            BLOCKING,
            "no negative control step",
            "Repeat the trigger as an identity that must be denied to show the effect is real.",
        )

    mutating = [index for index, step in enumerate(steps, start=1) if _method(step) in MUTATING_METHODS]
    cleanup = [item for item in _items(spec.get("cleanup")) if _text(item)]
    if mutating and not cleanup:
        add(
            "cleanup",
            BLOCKING,
            f"steps {mutating} mutate state but no cleanup is declared",
            "Delete what the PoC created and show the delete succeeded.",
        )

    evidence = [item for item in _items(spec.get("evidence")) if isinstance(item, dict)]
    if not evidence:
        add("evidence", BLOCKING, "no evidence entries")
    for index, item in enumerate(evidence, start=1):
        digest = _text(item.get("sha256"))
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest.lower()):
            add(
                "evidence-digest",
                BLOCKING,
                f"evidence {index} has no valid sha256",
                "Run `pocforge hash` so digests are computed, never typed by hand.",
            )
        if not _text(item.get("kind")):
            add("evidence-kind", MAJOR, f"evidence {index} does not name its kind")

    manifest_path = spec.get("evidence_manifest")
    if evidence_root is not None and _text(manifest_path):
        try:
            manifest_file = evidence_root / _text(manifest_path)
            problems = verify_manifest(
                json.loads(manifest_file.read_text(encoding="utf-8")),
                evidence_root,
                manifest_path=manifest_file,
            )
        except (EvidenceError, json.JSONDecodeError, OSError) as exc:
            add("evidence-verify", BLOCKING, f"evidence manifest cannot be verified: {exc}")
        else:
            for problem in problems:
                add("evidence-verify", BLOCKING, problem)

    impact = _impact(spec)
    if not _text(impact.get("what")) or not _text(impact.get("who")):
        add(
            "impact",
            MAJOR,
            "impact must name what an attacker gains and who is affected",
            "Triage severity follows the affected data and population, not the bug class.",
        )
    if _text(impact.get("severity_claim")).lower() not in SEVERITIES:
        add("impact-severity", MINOR, f"severity_claim must be one of {SEVERITIES}")

    reproduction = spec.get("reproduction")
    if not isinstance(reproduction, dict) or not (
        _text(reproduction.get("command")) or _text(reproduction.get("fixture"))
    ):
        add(
            "reproduction",
            MAJOR,
            "no reproduction command or fixture",
            "One command that a triager can paste is worth a page of prose.",
        )

    penalty = sum(PENALTY[item.severity] for item in findings)
    score = max(0, 100 - penalty)
    if any(item.severity == BLOCKING for item in findings):
        grade_letter = "D"
    elif score >= 90:
        grade_letter = "A"
    elif score >= 75:
        grade_letter = "B"
    elif score >= 55:
        grade_letter = "C"
    else:
        grade_letter = "D"

    return Report(spec_id=spec_id, score=score, grade=grade_letter, findings=findings)


def scaffold(title: str, spec_id: str = "new-poc") -> dict[str, Any]:
    """Return a spec skeleton that already passes the structural rules."""
    return {
        "schema": SCHEMA,
        "id": spec_id,
        "title": title,
        "target": {
            "base_url": "",
            "asset": "",
            "scope_ref": "",
            "authorized": False,
        },
        "preconditions": ["", ""],
        "steps": [
            {
                "n": 1,
                "action": "Authenticate as the owning identity and capture the baseline.",
                "request": {"method": "GET", "path": "/"},
                "expect": {"status": 200},
            },
            {
                "n": 2,
                "action": "Repeat the same request as the identity that must be denied.",
                "request": {"method": "GET", "path": "/"},
                "expect": {"status": 403},
                "control": True,
            },
            {
                "n": 3,
                "action": "Send the trigger and record the response verbatim.",
                "request": {"method": "GET", "path": "/"},
                "expect": {"status": 200},
            },
        ],
        "oracle": {
            "success": ["Step 3 returns the object owned by the other identity."],
            "failure": ["Step 3 returns 403 or 404, matching the control step."],
            "deterministic": True,
        },
        "control": "Step 2 is the negative control.",
        "cleanup": [],
        "evidence": [],
        "impact": {"what": "", "who": "", "severity_claim": "medium"},
        "reproduction": {"command": ""},
    }


def render_report(spec: dict[str, Any], report: Report) -> str:
    """Submission-shaped markdown, with the grade attached as an appendix."""
    target = _target(spec)
    impact = _impact(spec)
    lines = [
        f"# {_text(spec.get('title')) or report.spec_id}",
        "",
        f"**Spec:** `{report.spec_id}`  ",
        f"**Asset:** `{_text(target.get('asset')) or _text(target.get('base_url'))}`  ",
        f"**Scope reference:** {_text(target.get('scope_ref'))}",
        "",
        "## Summary",
        "",
        _text(spec.get("summary")) or "See steps.",
        "",
        "## Preconditions",
        "",
    ]
    lines += [f"- {item}" for item in _items(spec.get("preconditions"))] or ["- (none)"]
    lines += ["", "## Steps", ""]
    for step in _steps(spec):
        expect = step.get("expect")
        lines.append(
            f"{step.get('n')}. {_text(step.get('action'))} — expected `{json.dumps(expect, sort_keys=True)}`"
        )
    lines += ["", "## Oracle", ""]
    for label in ("success", "failure"):
        for item in _items(_oracle(spec).get(label)):
            lines.append(f"- **{label}**: {item}")
    lines += [
        "",
        "## Impact",
        "",
        f"- What: {_text(impact.get('what'))}",
        f"- Who: {_text(impact.get('who'))}",
        f"- Claimed severity: {_text(impact.get('severity_claim'))}",
        "",
        "## Reproduction",
        "",
        "```text",
        _text((spec.get("reproduction") or {}).get("command")) or "(none)",
        "```",
        "",
        "## Proof grade",
        "",
        f"- Grade: **{report.grade}** ({report.score}/100), submittable: "
        f"{'yes' if report.submittable else 'no'}",
    ]
    for finding in report.findings:
        lines.append(f"- `{finding.severity}` {finding.rule}: {finding.message}")
    lines.append("")
    return "\n".join(lines)


def digest_index(paths: Iterable[Path]) -> dict[str, Any]:
    """Evidence entries for a spec, built by hashing real files."""
    from .evidence import sha256_file

    entries = []
    for path in paths:
        if not path.is_file():
            raise EvidenceError(f"evidence file is missing: {path}")
        entries.append(
            {"kind": path.suffix.lstrip(".") or "file", "ref": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        )
    return {"evidence": entries}

"""pocforge command line interface.

Corpus commands (validate / list / show / search / build) come from the pack
harness. The domain commands grade a PoC against the rules that triagers apply:

    pocforge check poc.json
    pocforge check poc.json --evidence-root results --json
    pocforge hash results/ --write results/manifest.json
    pocforge verify results/manifest.json --root results
    pocforge scaffold "IDOR on order export" --id idor-order-export
    pocforge report poc.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .corpus import BY_SLUG, PACK, SKILLS
from .evidence import EvidenceError, build_manifest, load_manifest, verify_manifest, write_manifest
from .render import build_pack, render_skill, word_count
from .spec import SpecError, digest_index, grade, load_spec, render_report, scaffold
from .validate import (
    MAX_DESCRIPTION,
    MIN_DONE,
    MIN_PATTERNS,
    MIN_PITFALLS,
    MIN_SIGNALS,
    MIN_STEPS,
    MIN_SUMMARY,
    MIN_WORDS,
    Issue,
    validate_pack,
)

FLOORS = {
    "min_steps": MIN_STEPS,
    "min_signals": MIN_SIGNALS,
    "min_patterns": MIN_PATTERNS,
    "min_pitfalls": MIN_PITFALLS,
    "min_done_when": MIN_DONE,
    "min_summary_chars": MIN_SUMMARY,
    "min_words": MIN_WORDS,
    "max_description_chars": MAX_DESCRIPTION,
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _report(issues: list[Issue], total: int, as_json: bool, title: str) -> int:
    bad = {issue.slug for issue in issues if issue.slug}
    valid = total - len(bad)
    if as_json:
        print(
            json.dumps(
                {
                    "pack": title,
                    "checked": total,
                    "valid": valid,
                    "passed": not issues,
                    "floors": FLOORS,
                    "issues": [
                        {"slug": i.slug, "rule": i.rule, "message": i.message} for i in issues
                    ],
                },
                indent=2,
            )
        )
    else:
        print(f"{title}: {valid}/{total} skills valid")
        for issue in issues:
            print(f"  FAIL {issue}")
        if not issues:
            print(
                f"  ok  steps>={MIN_STEPS} signals>={MIN_SIGNALS} patterns>={MIN_PATTERNS} "
                f"pitfalls>={MIN_PITFALLS} words>={MIN_WORDS} refs canonical https"
            )
    return 0 if not issues else 1


def cmd_validate(args: argparse.Namespace) -> int:
    return _report(validate_pack(PACK, SKILLS), len(SKILLS), args.json, PACK["name"])


def cmd_list(args: argparse.Namespace) -> int:
    rows = [
        skill
        for skill in SKILLS
        if (not args.tag or args.tag in skill.tags)
        and (not args.phase or skill.meta_get("phase") == args.phase)
    ]
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "slug": s.slug,
                        "title": s.title,
                        "phase": s.meta_get("phase"),
                        "tags": list(s.tags),
                    }
                    for s in rows
                ],
                indent=2,
            )
        )
        return 0
    for skill in rows:
        print(f"{skill.meta_get('phase'):11s} {skill.slug:38s} {skill.title}")
    print(f"# {len(rows)} skill(s)")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    skill = BY_SLUG.get(args.slug)
    if skill is None:
        print(f"unknown skill: {args.slug}", file=sys.stderr)
        return 2
    text = render_skill(PACK, skill)
    print(text if args.raw else text.split("---\n", 2)[-1].lstrip())
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    terms = [term.lower() for term in args.terms]

    def score(skill) -> int:
        blob = " ".join(
            [skill.slug, skill.title, skill.summary, *skill.tags, *skill.steps]
        ).lower()
        return sum(blob.count(term) for term in terms)

    ranked = sorted(
        ((score(skill), skill) for skill in SKILLS if score(skill)),
        key=lambda pair: (-pair[0], pair[1].slug),
    )[: args.limit]
    if not ranked:
        print("no matches", file=sys.stderr)
        return 1
    for points, skill in ranked:
        print(f"{points:3d}  {skill.slug:38s} {skill.title}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else repo_root()
    written = build_pack(root, PACK, SKILLS)
    print(f"wrote {len(written)} file(s) under {root}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    try:
        spec = load_spec(Path(args.spec))
    except SpecError as exc:
        print(f"cannot read spec: {exc}", file=sys.stderr)
        return 2
    root = Path(args.evidence_root) if args.evidence_root else None
    report = grade(spec, evidence_root=root)
    if args.json:
        print(json.dumps(report.as_dict(), indent=2))
    else:
        print(f"{report.spec_id}: grade {report.grade} ({report.score}/100) "
              f"{'submittable' if report.submittable else 'NOT submittable'}")
        for finding in report.findings:
            print(f"  {finding.severity:8s} {finding.rule}: {finding.message}")
            if finding.hint and args.verbose:
                print(f"           -> {finding.hint}")
    return 0 if report.submittable else 1


def cmd_scaffold(args: argparse.Namespace) -> int:
    spec = scaffold(args.title, args.id)
    text = json.dumps(spec, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {args.out}")
    else:
        print(text, end="")
    return 0


def cmd_hash(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else None
    try:
        manifest = build_manifest(root, args.paths or None)
    except EvidenceError as exc:
        print(f"cannot hash evidence: {exc}", file=sys.stderr)
        return 2
    if args.write:
        write_manifest(manifest, Path(args.write))
        print(f"hashed {manifest['count']} file(s) into {args.write}")
    else:
        print(json.dumps(manifest, indent=2))
    if args.spec:
        spec_path = Path(args.spec)
        spec = load_spec(spec_path)
        base = Path(args.write).parent if args.write else (root or Path("."))
        files = [base / entry["path"] for entry in manifest["files"]]
        spec["evidence"] = digest_index(files)["evidence"]
        spec["evidence_manifest"] = Path(args.write).name if args.write else ""
        spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"attached {len(files)} evidence entr(ies) to {spec_path}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    try:
        manifest = load_manifest(Path(args.manifest))
    except EvidenceError as exc:
        print(f"cannot read manifest: {exc}", file=sys.stderr)
        return 2
    problems = verify_manifest(manifest, Path(args.root), manifest_path=Path(args.manifest))
    if problems:
        for problem in problems:
            print(f"FAIL {problem}")
        return 1
    print(f"ok  {manifest['count']} file(s) match {args.manifest}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    try:
        spec = load_spec(Path(args.spec))
    except SpecError as exc:
        print(f"cannot read spec: {exc}", file=sys.stderr)
        return 2
    report = grade(spec, evidence_root=Path(args.evidence_root) if args.evidence_root else None)
    text = render_report(spec, report)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {args.out}")
    else:
        print(text, end="")
    return 0 if report.submittable else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=PACK["name"], description=PACK["description"])
    parser.add_argument("--version", action="version", version=f"{PACK['name']} {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="run every corpus rule")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("list", help="list skills")
    p.add_argument("--tag", default=None)
    p.add_argument("--phase", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="print one SKILL.md")
    p.add_argument("slug")
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="rank skills by keyword")
    p.add_argument("terms", nargs="+")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("build", help="regenerate skills/, pack.json and results/")
    p.add_argument("--root", default=None)
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("check", help="grade a PoC spec")
    p.add_argument("spec")
    p.add_argument("--evidence-root", default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("scaffold", help="emit a spec skeleton that passes the structural rules")
    p.add_argument("title")
    p.add_argument("--id", default="new-poc")
    p.add_argument("--out", default=None)
    p.set_defaults(func=cmd_scaffold)

    p = sub.add_parser("hash", help="hash evidence files into a manifest")
    p.add_argument("paths", nargs="*")
    p.add_argument("--root", default=None)
    p.add_argument("--write", default=None)
    p.add_argument("--spec", default=None)
    p.set_defaults(func=cmd_hash)

    p = sub.add_parser("verify", help="re-hash evidence and report drift")
    p.add_argument("manifest")
    p.add_argument("--root", default=".")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("report", help="render submission markdown with the proof grade")
    p.add_argument("spec")
    p.add_argument("--evidence-root", default=None)
    p.add_argument("--out", default=None)
    p.set_defaults(func=cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

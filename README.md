# pocforge

Grade a bug-bounty proof of concept before a triager does.

`pocforge` is two things that share one corpus:

- **A PoC grader.** You describe the PoC as JSON — target, scope quote, steps, oracle, control, cleanup, evidence, impact — and it applies the rules triagers actually reject reports for. Output is a grade, a score and a list of findings with severities, so you fix the report instead of arguing about it.
- **50 skills** for building, minimizing and verifying PoCs, loaded by Claude Code, opencode or any agent runtime that reads `SKILL.md` files.

There are no dependencies. Python 3.10+ standard library, `pytest` for development.

```text
$ pocforge check examples/poc/idor-order-read.json --evidence-root examples/evidence
idor-order-read: grade A (100/100) submittable
```

```text
$ pocforge check results/_incomplete.json
draft: grade D (0/100) NOT submittable
  blocking scope-ref: target has no scope reference
  blocking authorized: target is not marked authorized
  major    preconditions: found 0 precondition(s), need 2
  blocking evidence: no evidence entries
  major    impact: impact must name what an attacker gains and who is affected
  major    reproduction: no reproduction command or fixture
```

## Why a grader

Most rejected reports fail for the same handful of reasons, and none of them are about the bug:

| Rule | Severity | What it catches |
|---|---|---|
| `scope-ref` | blocking | the asset is never tied to a scope line |
| `authorized` | blocking | testing was never confirmed as permitted |
| `steps` | blocking | fewer than three steps, so there is no setup/trigger/observe |
| `step-expect` | blocking | a step with no expected result cannot fail, so it proves nothing |
| `oracle` | blocking | only a success condition, so an error page counts as a win |
| `negative-control` | blocking | no denied identity to prove the boundary exists |
| `cleanup` | blocking | a mutating PoC leaves state behind |
| `evidence` / `evidence-digest` | blocking | no artifacts, or hand-typed digests |
| `evidence-verify` | blocking | the evidence changed after it was hashed |
| `impact` | major | impact does not name what is gained and who is affected |
| `reproduction` | major | no command or fixture a triager can run |
| `oracle-determinism` | major | a flaky trigger reported as certain |

Any blocking finding caps the grade at D. Score is 100 minus 25 per blocking, 10 per major and 3 per minor finding.

## Tamper-evident evidence

Hash the artifacts, attach them to the spec, and re-verify before submitting:

```text
$ pocforge hash examples/evidence --write examples/evidence/manifest.json --spec examples/poc/idor-order-read.json
hashed 3 file(s) into examples/evidence/manifest.json
attached 3 evidence entr(ies) to examples/poc/idor-order-read.json

$ pocforge verify examples/evidence/manifest.json --root examples/evidence
ok  3 file(s) match examples/evidence/manifest.json
```

Edit one byte of a capture and the next verification names the file, the old size and the new size. A manifest that lives inside the evidence directory does not try to hash itself, and any file added after hashing is reported as unrecorded rather than silently accepted.

## Commands

```text
pocforge check SPEC [--evidence-root DIR] [--json] [--verbose]   # grade a PoC
pocforge report SPEC [--out FILE]                               # submission markdown + grade
pocforge scaffold "Title" --id idor-order-export --out poc.json  # skeleton that passes structure
pocforge hash PATHS... --write manifest.json [--spec SPEC]       # hash and attach evidence
pocforge verify manifest.json --root DIR                         # re-hash and report drift
pocforge validate [--json]                                       # the 50/50 corpus gate
pocforge list [--phase oracle] [--tag authz]                     # browse skills
pocforge show SLUG                                               # one SKILL.md
pocforge search TERMS...                                         # rank skills by keyword
pocforge build                                                    # regenerate skills/ and pack.json
```

## The skills

50 skills, six phases, in lifecycle order:

| Phase | Count | What it covers |
|---|---|---|
| `frame` | 9 | scope quotation, asset mapping, claim versus effect, preconditions, identity matrix, dedupe, blast radius, severity mapping, stop conditions |
| `reproduce` | 9 | baselines, single-variable steps, frozen requests, state snapshots, minimal account pairs, determinism, timing windows, environment pinning, failed runs |
| `minimize` | 8 | step elimination, parameter and header reduction, payload bisection, account collapse, numeric bounds, artifact pruning, one-line repro |
| `oracle` | 8 | success/failure differentials, negative controls, cross-identity oracles, side effects, timing calibration, error oracles, nondeterminism budgets, second instances |
| `verify` | 8 | clean-state reruns, independent replay, patch rechecks, hash locks, scope drift, false-positive elimination, impact boundaries, regression scripts |
| `package` | 8 | manifests, screenshot provenance, redaction, step numbering, impact-first summaries, remediation, retest plans, disclosure timelines |

Each skill carries `use_when`, `avoid_when`, six or more steps, signals, three code patterns, pitfalls, done-when criteria and canonical https references. `pocforge validate` enforces the floors on every run, so the corpus cannot quietly degrade.

## Install

```bash
python -m pip install -e ".[dev]"
pocforge validate
python -m pytest -q
```

## Proof

`RESULTS.md` records the commands run for this release and their real output, including the tamper demo. The corpus gate is part of CI, along with a check that the committed `skills/` tree is byte-identical to a fresh render.

## Scope and intent

This is a reporting-quality tool. It has no network code, sends no requests and cannot test anything for you; it checks whether the evidence you already have would survive review. Every technique it documents assumes a program that authorizes the testing, which is exactly what the `authorized` and `scope-ref` rules exist to enforce.

MIT licensed.

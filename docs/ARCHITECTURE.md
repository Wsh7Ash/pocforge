# Architecture

`pocforge` has no runtime dependencies and no network access. It is a rule engine over two data shapes: a skill corpus and a PoC spec.

## Modules

| Module | Responsibility |
|---|---|
| `model.py` | `Skill` dataclass and the shape validation used when the corpus loads |
| `validate.py` | The 50/50 gate: structure, strength floors, hygiene rules |
| `render.py` | Deterministic `SKILL.md` rendering, `pack.json`, catalog, `build_pack` |
| `spec.py` | PoC spec rules, grading, submission markdown, scaffolding |
| `evidence.py` | Manifest construction, hashing, drift detection |
| `cli.py` | Argument parsing and the command surface |
| `corpus/part1..3.py` | The 50 skills as plain dicts |

## Data flow

```text
corpus/part*.py  ->  model.skill_from_dict  ->  validate.validate_pack  ->  render.build_pack
                                                     |                        |
                                                     v                        v
                                            results/validation.json     skills/, pack.json

poc.json  ->  spec.grade  ->  Report(grade, score, findings)  ->  cli.check / spec.render_report
                |
                v
        evidence.verify_manifest  <-  evidence/manifest.json
```

`render.build_pack` is the only writer of generated artifacts. Tests re-render every skill and compare bytes with the committed files, so the published corpus cannot drift from the source of truth.

## Grading model

Findings carry one of three severities:

- **blocking** — the report is not submittable as written (missing scope, no oracle, no control, uncontrolled mutation, unusable evidence).
- **major** — submittable but weak (no reproduction command, non-deterministic oracle, missing impact statement).
- **minor** — hygiene (step numbering, severity vocabulary).

Score is `max(0, 100 - 25*blocking - 10*major - 3*minor)`. Any blocking finding forces grade `D`, because a report that cannot be reproduced is not a report no matter how much prose it has. Grades A/B/C are score thresholds of 90/75/55.

The rule set deliberately separates two questions:

1. *Is this a valid vulnerability?* — out of scope for a linter; the researcher answers it with steps and a control.
2. *Is this PoC a valid proof of it?* — what every rule here checks.

## Evidence integrity

A manifest cannot hash itself, so `build_manifest` records paths relative to an inferred root and `verify_manifest` accepts the manifest's own path to exclude it from the unrecorded scan. Three failure modes are reported separately because they mean different things during triage:

| Problem | Meaning |
|---|---|
| `missing: path` | the artifact was never uploaded |
| `size changed` / `digest changed` | the artifact was edited after being cited |
| `unrecorded file` | an artifact was added after the set was locked |

## Deliberate non-goals

- No HTTP client. Sending requests is the researcher's job; `pocforge` judges the artifacts that come back.
- No severity calculator. Impact is a claim that must be backed by a step, not an arithmetic result.
- No template marketplace. A spec is a small JSON file you keep next to the evidence.

# Contributing

## Setup

```bash
python -m pip install -e ".[dev]"
pocforge validate
python -m pytest -q
```

The runtime is standard-library only. A pull request that adds a runtime dependency needs to explain why the stdlib is insufficient.

## What is welcome

- **A new grading rule.** Add it to `spec.py` with a severity, a message that names the missing artifact rather than the missing sentence, and a hint. Add a test that fails without the rule.
- **A stronger skill.** Skills are data; edit the relevant `corpus/part*.py` entry and rerun `pocforge build`.
- **A defect in the tool.** Repro command, observed output, expected output.

## What is not welcome

- Placeholder text, vague steps, or skills that restate the title.
- Severity inflation in the rules so that a weak report grades higher.
- Weakening a validator floor to fit a skill. Fix the skill.
- Network code. `pocforge` does not send requests, by design.

## Skill floors

`pocforge validate` enforces these on every run, and CI runs it before the tests:

| Field | Floor |
|---|---|
| steps | 6, each at least 25 characters |
| signals | 4 |
| patterns | 3, each with a label of 8+ characters and code of 20+ |
| pitfalls | 3, each at least 30 characters |
| done_when | 2 |
| tags | 2, lowercase kebab-case |
| refs | 1, formatted `[label](https://...)` |
| rendered words | 180 |

Also rejected: TODO/FIXME/TBD markers, machine-local paths, duplicate slugs or titles, and a missing `meta.phase`.

## After editing the corpus

```bash
pocforge build      # regenerate skills/, pack.json and results/catalog.md
pocforge validate   # the 50/50 gate
python -m pytest -q
```

Commit the regenerated files with the corpus change; CI fails on drift between the two.

## Adding a skill

1. Pick the phase that matches when the technique is used. `pocforge list` shows the current distribution.
2. Write the procedure as six or more imperative steps, each replayable.
3. Add one pattern per decision a reader has to make, as `(label, code)` where code is plain text, not fenced.
4. Run `pocforge build` and `pocforge validate`.

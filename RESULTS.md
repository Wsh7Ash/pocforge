# Results

Reproducible evidence for the claims in `README.md`. Every command below was run in this repository; output is verbatim.

## Environment

- OS: Windows (MSYS2 shell), CPython 3.14
- Runtime: Python 3.10+ standard library, `pytest` as the only development dependency
- Network: not required at any point

## Corpus gate

```text
$ pocforge validate
pocforge: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

`results/validation.json` is the machine-readable form of the same run: `checked 50, valid 50, passed true`.

Phase distribution (from `pocforge list`, grouped by `meta.phase`): `frame` 9, `reproduce` 9, `minimize` 8, `oracle` 8, `verify` 8, `package` 8.

## Test suite

```text
$ python -m pytest -q
...........................                                              [100%]
```

27 tests, covering the corpus gate, committed-artifact drift, every grading rule, the evidence manifest, tamper detection and the CLI.

## Grader, end to end

`results/demo_transcript.txt` is a real session. The short form:

| Command | Result |
|---|---|
| `check examples/poc/idor-order-read.json --evidence-root examples/evidence` | `grade A (100/100) submittable`, exit 0 |
| `check` on a scaffolded draft with no scope line | `grade D (0/100) NOT submittable`, 6 findings, exit 1 |
| `verify examples/evidence/manifest.json` | `ok 3 file(s) match`, exit 0 |
| `verify` after appending one byte to a capture | `FAIL size changed: step-03-trigger.http (221 -> 222 bytes)` and `FAIL digest changed`, exit 1 |
| `verify` after restoring the capture | `ok 3 file(s) match`, exit 0 |

## Defects found and fixed during this build

These are real bugs the tests and demos surfaced, not hypotheticals:

1. **Manifest paths were recorded relative to the caller's cwd.** Hashing `examples/evidence` from the repository root produced entries like `examples/evidence/step-02-control.http`, so `verify --root examples/evidence` looked for `examples/evidence/examples/evidence/...` and reported every file missing. Fixed by inferring the manifest root from the collected files and always recording paths relative to it.
2. **A manifest stored inside the evidence directory flagged itself.** The unrecorded-file scan counted `manifest.json`, which cannot contain its own digest. `verify_manifest` now takes the manifest path and skips it.
3. **`hash` refused a directory argument.** Passing the evidence directory raised `evidence file is missing: examples/evidence`. Directory arguments are now expanded into their files.
4. **`infer_root` could loop forever** when two files shared no common parent under the current drive root, because the walk never terminated. It now stops at the filesystem root and falls back to the current directory.

## What is not verified

- No live target was contacted. The tool has no network code, so the example spec grades a synthetic capture set by design.
- The grading rules encode reporting practice, not a specific program's policy; a program with different rules would need different severities.

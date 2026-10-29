# Examples

A synthetic cross-tenant IDOR to exercise the grader end to end. Everything here is invented: `example.test` hosts, placeholder tokens, no real data.

| Path | What it is |
|---|---|
| `poc/idor-order-read.json` | A complete PoC spec: four numbered steps, a negative control, both oracle sides, cleanup, impact and a reproduction command |
| `evidence/step-02-control.http` | The control request and its 404 response |
| `evidence/step-03-trigger.http` | The trigger request and the 200 carrying alice's marker |
| `evidence/cleanup-204.http` | The delete that removes what the PoC created |
| `evidence/manifest.json` | SHA-256, size and path for each artifact |

## Run it

```bash
pocforge check examples/poc/idor-order-read.json --evidence-root examples/evidence
# idor-order-read: grade A (100/100) submittable

pocforge verify examples/evidence/manifest.json --root examples/evidence
# ok  3 file(s) match examples/evidence/manifest.json

pocforge report examples/poc/idor-order-read.json --evidence-root examples/evidence
```

## Break it on purpose

The fastest way to understand the rules is to remove one element and watch the grade fall:

```bash
# no negative control
python - <<'PY'
import json
spec = json.load(open("examples/poc/idor-order-read.json"))
for step in spec["steps"]:
    step.pop("control", None)
spec.pop("control", None)
json.dump(spec, open("results/no-control.json", "w"), indent=2)
PY
pocforge check results/no-control.json --evidence-root examples/evidence
# grade D, blocking negative-control
```

Or tamper with a capture:

```bash
printf 'x' >> examples/evidence/step-03-trigger.http
pocforge verify examples/evidence/manifest.json --root examples/evidence
# FAIL size changed: step-03-trigger.http (221 -> 222 bytes)
```

Restore the file (remove the appended byte) and verification passes again.

## Regenerating the manifest

If you change an artifact deliberately:

```bash
pocforge hash examples/evidence --write examples/evidence/manifest.json --spec examples/poc/idor-order-read.json
```

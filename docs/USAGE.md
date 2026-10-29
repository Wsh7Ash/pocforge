# Usage

## 1. Scaffold a spec

```bash
pocforge scaffold "Cross-tenant read of order records" --id idor-order-read --out poc.json
```

The skeleton already satisfies the structural rules, including a control step. It still fails on scope, authorization and evidence, which is the point: those are decisions only you can make.

## 2. Fill in the parts that only you can answer

```json
{
  "target": {
    "asset": "https://api.example.test/v2/orders",
    "scope_ref": "asset: api.example.test (wildcard, one label deep), captured 2026-10-29T09:12Z",
    "authorized": true
  },
  "oracle": {
    "success": ["step 3 returns 200 and the body contains alice's marker POC-ALICE-7741"],
    "failure": ["step 3 returns 404 or 403, matching the control in step 2"],
    "deterministic": true
  },
  "impact": {
    "what": "order records including customer email and phone, readable across tenants",
    "who": "every tenant with at least one member, since ids are sequential",
    "severity_claim": "high"
  }
}
```

The `oracle` block is the part researchers skip and triagers reject. Write both sides: the condition that means the effect happened, and the condition that means it did not. A 500 response that a reader could interpret either way is neither.

## 3. Grade it

```bash
pocforge check poc.json
pocforge check poc.json --json | jq '.findings[] | select(.severity == "blocking")'
```

Iterate until there are no blocking findings. `--verbose` prints the hint for each finding, which usually names the missing request rather than the missing sentence.

## 4. Hash the evidence

```bash
pocforge hash evidence/ --write evidence/manifest.json --spec poc.json
pocforge verify evidence/manifest.json --root evidence
```

`hash` computes digests, writes the manifest, and rewrites the spec's `evidence` array from the real files, so no digest is ever typed by hand. `verify` re-hashes and reports drift.

Keep the manifest inside the evidence directory if you like; it excludes itself from the scan. If you add a file after hashing, `verify` calls it unrecorded instead of ignoring it.

## 5. Render the submission

```bash
pocforge report poc.json --out report.md
```

The output is ordered for a triager: title, asset, scope reference, summary, preconditions, numbered steps with expected results, oracle, impact, reproduction command, then the proof grade as an appendix.

## Using the skills

```bash
pocforge list --phase oracle
pocforge show negative-control-step
pocforge search "timing" "race"
```

Skills live at `skills/<slug>/SKILL.md`, with YAML front matter and sections for procedure, signals, patterns, pitfalls, done-when and references. Any agent runtime that loads `SKILL.md` files can use them directly; `pack.json` carries a SHA-256 per file so an agent can verify what it loaded.

A full pass over one finding:

```bash
pocforge show scope-line-quotation          # frame
pocforge show baseline-capture-first        # reproduce
pocforge show step-elimination-sweep        # minimize
pocforge show negative-control-step         # oracle
pocforge show evidence-hash-lock            # verify
pocforge show impact-first-summary          # package
```

## Reading a grade

| Grade | Score | Meaning |
|---|---|---|
| A | 90-100 | submittable as written |
| B | 75-89 | submittable, weak on major rules |
| C | 55-74 | several majors; a triager will ask questions |
| D | any blocking finding, or below 55 | not submittable |

A `D` with a score of 75 is a well-written report missing one blocking element, usually a negative control. That distinction is why the grade and the score are reported separately.

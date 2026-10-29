---
name: scope-drift-recheck
description: "Re-read the program scope immediately before submitting, because programs add exclusions mid-engagement and a stale quote turns a valid report into an out-of-scope one. Use when the PoC was built days or weeks before submission, or the program was recently updated"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, scope, triage]
---

# Scope Drift Recheck

> Re-read the program scope immediately before submitting, because programs add exclusions mid-engagement and a stale quote turns a valid report into an out-of-scope one

**Use when:** the PoC was built days or weeks before submission, or the program was recently updated

**Avoid when:** the report is submitted within hours of the scope check

## Procedure

1. Open the program scope page and compare it with the quote stored in the spec.
2. Check the exclusions list for any new path that covers your trigger.
3. Check the asset list for the host, including wildcard depth.
4. Look for a new duplicate or known-issues note matching your finding.
5. Update the spec with the fresh quote and timestamp, or withdraw the report.
6. Note the drift explicitly if the scope changed in a way that still leaves you covered.

## Signals

- The exclusions list grew since your first capture.
- The asset moved from covered to out of scope with a grace period note.
- A new known-issues entry names your endpoint.
- The program switched to a different platform with a fresh scope table.

## Patterns

**1. Compare quotes**

```text
captured: asset: api.example.com/exclusions: /v2/admin
now:      exclusions: /v2/admin, /v2/export  -> your export trigger is now excluded
```

**2. Grace period**

```text
program note: findings reported before 2026-10-20 still accepted  -> cite it
```

**3. Withdraw rather than argue**

```text
if the path is now excluded, report the scope change as feedback, not as a bug
```

## Pitfalls

- Submitting against a scope quote captured before a program update.
- Missing a known-issues entry that names your exact finding class.
- Arguing scope in the report instead of checking whether a grace period applies.

## Done when

- The spec holds a scope quote retrieved within twenty-four hours of submission.
- Any drift is recorded with its effect on the finding.

## References

- [HackerOne - scope changes](https://docs.hackerone.com/en/articles/8475114-scope)
- [Bugcrowd - program updates](https://docs.bugcrowd.com/researchers/reporting-managing-submissions/scope/)

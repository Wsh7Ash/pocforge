---
name: remediation-suggestion
description: "Offer a fix that matches the demonstrated root cause and does not break the legitimate path, which shortens the fix cycle and raises report quality. Use when the root cause is clearly identified, such as a missing ownership check on one route"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, remediation, writing]
---

# Remediation Suggestion

> Offer a fix that matches the demonstrated root cause and does not break the legitimate path, which shortens the fix cycle and raises report quality

**Use when:** the root cause is clearly identified, such as a missing ownership check on one route

**Avoid when:** the root cause is still unknown and a guess would misdirect the vendor's engineers

## Procedure

1. State the root cause in one sentence tied to the observed request.
2. Describe the check that should exist and where it belongs in the request lifecycle.
3. Note the legitimate path that must keep working after the fix.
4. Suggest a test the vendor can add, phrased as the denied case plus the allowed case.
5. Avoid prescribing a library or framework change the codebase may not support.
6. Offer the regression script from the verify phase as the acceptance test.

## Signals

- The same check exists on a sibling route, which gives the vendor a model to copy.
- The fix is one condition in an existing authorization helper.
- A framework middleware already provides the missing check globally.
- The root cause is a data-model issue that a route-level fix would only mask.

## Patterns

**1. Root cause to check**

```text
root cause: GET /orders/{id} loads by id without filtering on tenant
dfix: scope the query by the authenticated tenant, return 404 on mismatch
```

**2. Keep the legit path**

```text
alice's own order must still return 200 with the same body
```

**3. Acceptance test**

```text
denied case returns 404; allowed case returns 200; regression script exits zero in fixed mode
```

## Pitfalls

- Prescribing a rewrite for a one-line check, which reads as not understanding the codebase.
- Suggesting a fix that would break the legitimate path you demonstrated.
- Guessing the fix when the root cause was never established, misdirecting the vendor.

## Done when

- The suggested check is tied to the demonstrated root cause.
- The suggestion names both the denied case and the path that must keep working.

## References

- [OWASP - authorization cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [CWE-285 - improper authorization](https://cwe.mitre.org/data/definitions/285.html)

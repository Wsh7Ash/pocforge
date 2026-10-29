---
name: retest-plan-attachment
description: "Attach a short plan for how the fix will be verified, so the retest is a scheduled step rather than an afterthought. Use when the program runs a fix-then-verify cycle and expects the researcher to retest"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, retest, planning]
---

# Retest Plan Attachment

> Attach a short plan for how the fix will be verified, so the retest is a scheduled step rather than an afterthought

**Use when:** the program runs a fix-then-verify cycle and expects the researcher to retest

**Avoid when:** the program closes reports without retest and the plan would never be used

## Procedure

1. List the exact requests that will be replayed after the patch.
2. State the expected response for each one when the fix is correct.
3. Identify how the deployed build will be confirmed, such as a version endpoint.
4. Include the regression script and its two modes.
5. Note the legitimate-path checks that must still pass.
6. Add a reminder date and the scope-recheck step before the retest.

## Signals

- The retest plan needs a step you cannot perform without vendor help.
- The expected fixed response is not currently defined anywhere.
- The build cannot be identified from outside, so patch confirmation will be guesswork.
- The legitimate path was never tested before the fix, so there is no baseline.

## Patterns

**1. Request, expected**

```text
GET /orders/1042 as bob -> 404 (fixed)
GET /orders/1042 as alice -> 200 (unchanged)
```

**2. Confirm the build**

```text
GET /healthz -> version matches the fixed release
```

**3. Schedule it**

```text
retest due 2026-11-12; recheck scope first; run repro.sh --expect fixed
```

## Pitfalls

- Planning a retest that depends on the vendor telling you when the fix shipped.
- Forgetting the legitimate-path check, so a regression looks like success.
- Skipping the scope recheck, which can invalidate the retest itself.

## Done when

- The plan lists each request, its expected fixed response and the build check.
- The regression script is referenced with both modes.

## References

- [OWASP - vulnerability management lifecycle](https://owasp.org/www-community/vulnerability_management)
- [CWE - remediation guidance](https://cwe.mitre.org/)

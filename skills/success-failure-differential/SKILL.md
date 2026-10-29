---
name: success-failure-differential
description: "Define both a success condition and a failure condition for the trigger, so the PoC can distinguish a real effect from an unrelated error page. Use when the trigger response could plausibly be explained by a validation error, a rate limit or a generic 500"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, verification, method]
---

# Success Failure Differential

> Define both a success condition and a failure condition for the trigger, so the PoC can distinguish a real effect from an unrelated error page

**Use when:** the trigger response could plausibly be explained by a validation error, a rate limit or a generic 500

**Avoid when:** the success condition is already unambiguous, such as a 200 carrying another tenant's data

## Procedure

1. Write the exact field, status or byte pattern that means the effect occurred.
2. Write the exact pattern that means it did not, including the most likely benign explanation.
3. Send the trigger and check which pattern matched.
4. Send the control request and confirm the failure pattern matches there.
5. Reject any run that matches neither pattern as inconclusive and investigate.
6. Put both patterns in the oracle block of the spec, not in prose.

## Signals

- A 200 response contains an error object in the body.
- The effect pattern also matches the control response.
- A 500 response is being read as proof of exploitation.
- The response contains no field that distinguishes the two cases.

## Patterns

**1. Both sides written down**

```text
success: body.owner_id == "alice" and status == 200
failure: status in (403, 404) or body.error is present
```

**2. Reject the ambiguous middle**

```text
status 500 with a stack trace -> neither success nor failure -> investigate, do not report
```

**3. Control must match failure**

```text
control (bob's own order) -> success pattern
control (carol cross-tenant) -> failure pattern  -> as designed
```

## Pitfalls

- Treating any non-403 response as proof, including 500s and rate-limit pages.
- Writing only the success condition so a failed run looks like a success.
- Defining the oracle in prose that two readers would interpret differently.

## Done when

- The oracle block contains both a success and a failure pattern.
- A control run matches the failure pattern as written.

## References

- [OWASP WSTG - testing for error handling](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/)
- [CWE-209 - error message information leak](https://cwe.mitre.org/data/definitions/209.html)

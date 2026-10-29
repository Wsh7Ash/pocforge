---
name: account-collapse-test
description: "Check whether the effect still appears when both actors are the same account, which separates a real authorization bug from a confused-state artifact. Use when the PoC uses two accounts and you have not confirmed the effect depends on the identity difference"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, authz, false-positive]
---

# Account Collapse Test

> Check whether the effect still appears when both actors are the same account, which separates a real authorization bug from a confused-state artifact

**Use when:** the PoC uses two accounts and you have not confirmed the effect depends on the identity difference

**Avoid when:** the effect is definitionally cross-account, such as reading a record that only exists in another tenant

## Procedure

1. Re-send the trigger using the owning account for both the setup and the trigger.
2. Compare the response with the cross-account result.
3. If both succeed identically, the effect does not depend on identity and the claim is wrong.
4. If only the cross-account case succeeds, identity is load-bearing and the finding stands.
5. Record both responses as a pair in the evidence set.
6. Re-check the expected status for the same-account case before calling it a bug.

## Signals

- The same account can already read the object, so nothing crossed a boundary.
- The cross-account response is identical byte for byte to the same-account one.
- A shared link or public flag makes the object readable regardless of identity.
- The second account was a member of the same team with equal permissions.

## Patterns

**1. Collapse the actors**

```text
alice -> /orders/1042 -> 200 (expected, she owns it)
bob   -> /orders/1042 -> 200 (unexpected)
alice -> /orders/1042 -> 200 (collapse: proves nothing new)
```

**2. Look for a shared grant**

```text
order.shared_with = ["team-a"]  -> bob's access may be intended
```

**3. Pair the responses**

```text
evidence: results/collapse-same-account.http and results/collapse-cross-account.http
```

## Pitfalls

- Comparing against the wrong expected status for the owning account and inventing a boundary.
- Missing a team or shared-link grant that legitimately authorizes the second account.
- Treating a difference in response size as a difference in authorization.

## Done when

- Same-account and cross-account responses are both saved and compared.
- The spec states which comparison proved an authorization boundary was crossed.

## References

- [OWASP - broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [CWE-639 - authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)

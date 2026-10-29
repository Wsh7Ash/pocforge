---
name: identity-matrix-definition
description: "Define the smallest set of identities that proves an authorization difference, and state which pair owns the object and which pair must be denied. Use when the finding is an access-control difference and the writeup must show who should have been allowed and who was not"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [authz, frame, oracle]
---

# Identity Matrix Definition

> Define the smallest set of identities that proves an authorization difference, and state which pair owns the object and which pair must be denied

**Use when:** the finding is an access-control difference and the writeup must show who should have been allowed and who was not

**Avoid when:** the bug is a parser or injection flaw with no authorization dimension, where a second identity adds no information

## Procedure

1. Pick two accounts in the same tenant with different roles, and one account in a different tenant.
2. Assign each account a fixed label that the steps will reuse, such as owner, peer and outsider.
3. Identify which account owns the target object before sending anything.
4. Decide in advance which account the request must be denied to, and record that expectation.
5. Send the identical request as each identity, changing only the credential.
6. Report the matrix as a table so a triager can see the difference at a glance.

## Signals

- The response differs only by data content, not by status, between identities.
- The outsider account receives the same body as the owner.
- A peer with fewer permissions gets more data than the owner.
- Removing the credential entirely returns 200 with data instead of 401.

## Patterns

**1. Three-identity matrix**

```text
owner   alice  GET /orders/1042 -> 200 own data
peer    bob    GET /orders/1042 -> 200 alice's data  <- finding
outsider carol GET /orders/1042 -> 404
```

**2. Hold the request constant**

```text
same method, path, headers and body; only the Authorization value changes between rows
```

**3. Say which row is wrong**

```text
expected: peer -> 403, outsider -> 404
observed: peer -> 200, outsider -> 404  -> the peer row is the defect
```

## Pitfalls

- Using two accounts in different tenants and calling it a role check, when tenant isolation already covers it.
- Changing the path as well as the identity, which makes the two responses incomparable.
- Forgetting the unauthenticated row, which often shows the check is missing entirely.

## Done when

- A matrix lists every identity, the identical request and the observed status.
- The spec states which row violated the expected authorization decision.

## References

- [OWASP - broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [PortSwigger - access control vulnerabilities](https://portswigger.net/web-security/access-control)

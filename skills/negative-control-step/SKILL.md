---
name: negative-control-step
description: "Add the step that must be denied, so the writeup proves the server can enforce the rule it failed to enforce for your identity. Use when the finding is an access-control gap and the reader needs to see the denied case next to the allowed one"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, authz, control]
---

# Negative Control Step

> Add the step that must be denied, so the writeup proves the server can enforce the rule it failed to enforce for your identity

**Use when:** the finding is an access-control gap and the reader needs to see the denied case next to the allowed one

**Avoid when:** the effect is a global failure such as a crash on a public endpoint with no authorization dimension

## Procedure

1. Pick an identity that must be denied the same request under the product's own rules.
2. Send the identical request as that identity, changing only the credential.
3. Confirm the response is a denial, such as 403, 404 or a redirect to login.
4. Place the control step immediately before the triggering step in the PoC.
5. Reference the control response from the oracle's failure condition.
6. If the control is also allowed, stop: the rule does not exist and the finding changes class.

## Signals

- The control identity is also allowed, which means no boundary exists to cross.
- The control returns 404 while the trigger returns 200, the classic IDOR shape.
- The control redirects to login, proving authentication is enforced but authorization is not.
- The control is denied only for one HTTP method, hinting at method-based checks.

## Patterns

**1. Control then trigger**

```text
step 2 (control): carol GET /orders/1042 -> 404
step 3 (trigger): bob   GET /orders/1042 -> 200 with alice's data
```

**2. Same request, different key**

```text
identical path, headers and body; only the Authorization header differs
```

**3. Control can invalidate**

```text
if carol also gets 200, the endpoint is public by design  -> not a bug
```

## Pitfalls

- Using a control identity that is a teammate with equal rights, so a denial never happens.
- Changing the request along with the identity, which breaks the comparison.
- Reporting without a control and relying on the triager to assume the rule exists.

## Done when

- A control step exists and is denied for the reason the product intends.
- The oracle cites the control response as the failure condition.

## References

- [PortSwigger - access control labs](https://portswigger.net/web-security/access-control)
- [OWASP - authorization testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/)

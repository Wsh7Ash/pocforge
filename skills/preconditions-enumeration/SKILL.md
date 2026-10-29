---
name: preconditions-enumeration
description: "Enumerate every account, role, seed record and configuration the PoC silently depends on, because a triager who cannot recreate the starting state cannot reproduce the bug. Use when the trigger only works for a specific role, a pre-existing record, a feature flag or a paid plan tier"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, frame, triage]
---

# Preconditions Enumeration

> Enumerate every account, role, seed record and configuration the PoC silently depends on, because a triager who cannot recreate the starting state cannot reproduce the bug

**Use when:** the trigger only works for a specific role, a pre-existing record, a feature flag or a paid plan tier

**Avoid when:** the PoC runs against an anonymous request with no stored state, where the list would be empty

## Procedure

1. List each identity the PoC uses, with its role, plan tier and tenant.
2. List each record the PoC needs to exist before step 1, including its owner.
3. List each server-side toggle that must be on, such as a beta flag or a per-tenant setting.
4. Note anything you created during exploration that a fresh account would not have.
5. Add setup steps or a seed fixture for every item, so the spec stands alone.
6. Delete preconditions you cannot recreate and re-check whether the trigger still fires.

## Signals

- The bug only reproduces on the account you have been using for weeks.
- A record id from an earlier session appears in step 1 without a creation step.
- The trigger needs a paid plan, an admin role or an invited teammate.
- A feature flag was enabled for your tenant by support during testing.

## Patterns

**1. Identity table**

```text
alice  owner   tenant A  plan pro
bob    member  tenant A  plan pro
carol  owner   tenant B  plan free  -> carol is the control, never the trigger
```

**2. Seed before trigger**

```text
1. alice POST /orders {"sku":"A1"} -> 201, id captured as {{order_id}}
2. bob GET /orders/{{order_id}} -> the actual test
```

**3. Flag dependency is a precondition**

```text
precondition: tenant setting exports.beta = true (observed on alice's tenant only)
```

## Pitfalls

- Omitting a role that only exists because you were invited to a test tenant months ago.
- Assuming a fresh account inherits the same feature flags as your long-lived one.
- Burying a required record creation inside prose instead of making it a numbered step.

## Done when

- A researcher with two fresh accounts can recreate the starting state from the spec alone.
- Every identity, record and toggle the trigger needs appears in the preconditions list.

## References

- [OWASP WSTG - testing for business logic](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)
- [HackerOne - writing a good report](https://docs.hackerone.com/en/articles/8475114-scope)

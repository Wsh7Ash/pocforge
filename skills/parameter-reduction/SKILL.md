---
name: parameter-reduction
description: "Drop request parameters one at a time until the smallest set that still triggers the defect remains, which usually sharpens the root cause. Use when the request carries a dozen JSON keys or query parameters and the writeup blames the wrong one"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, parameters, method]
---

# Parameter Reduction

> Drop request parameters one at a time until the smallest set that still triggers the defect remains, which usually sharpens the root cause

**Use when:** the request carries a dozen JSON keys or query parameters and the writeup blames the wrong one

**Avoid when:** the endpoint validates a strict schema and rejects anything smaller than the full body

## Procedure

1. List every parameter in the working request with its current value.
2. Remove one parameter and re-send, keeping everything else identical.
3. Record whether the effect survives, changes shape or disappears.
4. Keep only parameters whose removal breaks the effect or changes its class.
5. For numeric parameters, try the smallest and largest values that still work.
6. Re-check the surviving set against the endpoint's documentation to name the root cause.

## Signals

- A parameter unrelated to the endpoint's purpose is silently accepted.
- Removing an optional field changes an error message, revealing validation order.
- The effect survives with an empty body, which points at a server-side default.
- A numeric parameter accepts negative or zero values without complaint.

## Patterns

**1. Removal matrix**

```text
keep: tenant_id, role
drop: locale, timezone, avatar_url
effect gone without tenant_id -> tenant_id is load-bearing
```

**2. Probe boundaries**

```text
qty: -1 accepted, 0 accepted, 999999999 accepted  -> no server-side bound
```

**3. Unexpected field wins**

```text
endpoint documents sku and qty;
body also sends price -> price is honoured  <- the actual bug
```

## Pitfalls

- Reducing the body until the schema rejects it and concluding the parameter is required.
- Assuming the documented parameter list is the accepted parameter list.
- Removing authentication fields along with body fields and confusing the two failures.

## Done when

- The reduced request contains only parameters proven load-bearing.
- Any undocumented field that changes behaviour is called out explicitly.

## References

- [OWASP - mass assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [PortSwigger - API testing](https://portswigger.net/web-security/api-testing)

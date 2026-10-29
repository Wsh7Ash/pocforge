---
name: impact-boundary-test
description: "Find the exact limit of what the defect allows, so the report claims the boundary instead of the most dramatic thing that might be true. Use when the effect lets you read or change more than one object and the report needs a defensible ceiling"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, impact, triage]
---

# Impact Boundary Test

> Find the exact limit of what the defect allows, so the report claims the boundary instead of the most dramatic thing that might be true

**Use when:** the effect lets you read or change more than one object and the report needs a defensible ceiling

**Avoid when:** the defect is strictly single-object by construction, such as one leaked static file

## Procedure

1. Start from the demonstrated effect and name the next capability it might unlock.
2. Design the smallest request that would prove that next capability.
3. Run it inside scope and record whether it succeeded.
4. Repeat for read, write and delete separately, since they often have different checks.
5. Stop at the first capability you cannot demonstrate and state it as the boundary.
6. Report the verified capability and mark everything beyond it as untested.

## Signals

- Read works cross-tenant but write returns 403, a clean boundary.
- Delete succeeds for objects you own but not for others.
- The check exists on the item route but not on the collection route.
- A bulk endpoint ignores the per-object check entirely.

## Patterns

**1. Test each capability**

```text
read   -> 200 cross-tenant
write  -> 403 cross-tenant
delete -> 404 cross-tenant  -> boundary: read only
```

**2. Collection versus item**

```text
GET /orders/1042 -> 403
GET /orders?tenant=B -> 200  -> the list route is the weak one
```

**3. State the ceiling**

```text
verified: cross-tenant read of order metadata
untested: bulk export, admin routes
```

## Pitfalls

- Claiming write impact because read worked and the endpoint looks symmetric.
- Stopping at read when a list endpoint quietly returns the same data in bulk.
- Testing the boundary by deleting another tenant's data, which breaks the stop condition.

## Done when

- Each capability is tested separately and its outcome recorded.
- The report states a verified ceiling and what remains untested.

## References

- [OWASP - broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [CWE-285 - improper authorization](https://cwe.mitre.org/data/definitions/285.html)

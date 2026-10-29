---
name: second-instance-confirmation
description: "Confirm the effect on a second object or account, so a one-off data artifact cannot be mistaken for a systemic authorization gap. Use when the finding rests on a single object whose access rules might be special, such as a shared or legacy record"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, verification, false-positive]
---

# Second Instance Confirmation

> Confirm the effect on a second object or account, so a one-off data artifact cannot be mistaken for a systemic authorization gap

**Use when:** the finding rests on a single object whose access rules might be special, such as a shared or legacy record

**Avoid when:** the single object is the entire impact, such as one leaked credential file

## Procedure

1. Create a second object of the same type, owned by a different identity than the first.
2. Repeat the exact same trigger against the second object with a fresh extract.
3. Confirm the response has the same shape and the same effect class.
4. Repeat once more with an object created after the test began, to rule out migration artifacts.
5. Record all three results, including any that behave differently.
6. State in the report whether the effect is systemic or limited, with counts.

## Signals

- The second object returns 403, meaning the first object had special sharing.
- All tested objects behave identically, which supports a systemic claim.
- A newly created object behaves differently from an old one, pointing at a backfill issue.
- The effect appears only on objects created through one specific flow.

## Patterns

**1. Three objects, three owners**

```text
order 1042 (alice, old)
order 1180 (bob, new)
order 1201 (carol, created during test)  -> same effect each time
```

**2. Report the proportion**

```text
3 of 3 objects readable across tenants  -> systemic, not a special record
```

**3. Flag the exception**

```text
1 of 3 returned 403 -> the object had explicit sharing  -> note it
```

## Pitfalls

- Generalising from one legacy object that happens to be shared by design.
- Using the same id twice by copying a stale extract and believing you tested twice.
- Hiding the object that behaved differently, which is exactly what triage will find.

## Done when

- At least two independently owned objects show the effect or the exception is explained.
- The report states whether the defect is systemic or object-specific.

## References

- [CWE-639 - authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)
- [OWASP - access control testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/)

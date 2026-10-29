---
name: cross-identity-oracle
description: "Make another identity's data the proof itself, by checking that the response contains a value only that identity could have produced. Use when the returned object looks plausible for either identity and status codes alone cannot tell them apart"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, authz, evidence]
---

# Cross Identity Oracle

> Make another identity's data the proof itself, by checking that the response contains a value only that identity could have produced

**Use when:** the returned object looks plausible for either identity and status codes alone cannot tell them apart

**Avoid when:** the response carries no identity-specific field and objects are indistinguishable in content

## Procedure

1. Give the victim identity a unique marker, such as a distinctive display name or note.
2. Perform the trigger as the attacker identity and capture the body.
3. Search the body for the victim's marker rather than for a generic field.
4. Confirm the attacker's own marker is absent from the same response.
5. Record both markers in the evidence file so a reader can see the discrimination.
6. Use the marker presence as the success condition in the oracle block.

## Signals

- The response contains an email or phone belonging to the other identity.
- The attacker's own id appears where the victim's should be, indicating a filter bug.
- The body includes a private note the victim wrote.
- A nested object carries the victim's tenant id.

## Patterns

**1. Plant a marker**

```text
alice sets display_name = POC-ALICE-7741
trigger as bob -> body contains POC-ALICE-7741
```

**2. Check both directions**

```text
victim marker present AND attacker marker absent  -> unambiguous
```

**3. Cite the marker**

```text
oracle.success: body contains POC-ALICE-7741
```

## Pitfalls

- Searching for a common field like email and matching the attacker's own address.
- Forgetting that a shared team view legitimately lists both members.
- Using a marker that the UI truncates, so a substring search misses it.

## Done when

- The success condition names a value only the victim identity could supply.
- The evidence file shows the victim marker in the attacker's response.

## References

- [CWE-639 - authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)
- [OWASP - insecure direct object reference](https://owasp.org/www-community/vulnerabilities/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet)

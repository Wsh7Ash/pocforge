---
name: state-snapshot-before-trigger
description: "Record the object's state immediately before the trigger, so the after-state diff is evidence of what the request changed rather than a story about it. Use when the defect changes server state, such as a role, balance, ownership, visibility or status field"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, evidence, state]
---

# State Snapshot Before Trigger

> Record the object's state immediately before the trigger, so the after-state diff is evidence of what the request changed rather than a story about it

**Use when:** the defect changes server state, such as a role, balance, ownership, visibility or status field

**Avoid when:** the effect is purely a response-body disclosure with no persistent change

## Procedure

1. Read the target object through a legitimate path and save the full representation.
2. Note the fields you expect the trigger to change and their current values.
3. Send the trigger request and capture its response.
4. Re-read the same object through the legitimate path, as the same identity as before.
5. Diff before and after and list only the fields that actually moved.
6. Attach both representations and the diff to the evidence set.

## Signals

- The trigger returns 200 but the object is unchanged afterwards.
- A field changes that you did not expect, which may be a stronger finding.
- The object is readable by a different identity after the trigger but not before.
- The response body claims success while the re-read disagrees.

## Patterns

**1. Before and after read**

```text
before: {"role":"member","tenant":"A"}
trigger: PATCH /users/{{bob}} {"role":"owner"}
after:  {"role":"owner","tenant":"A"}
```

**2. Diff only what moved**

```text
changed: role
unchanged: tenant, email, created_at  -> claim only the role escalation
```

**3. Re-read as the same identity**

```text
use alice's token for both reads  -> removes authorization as a confounder
```

## Pitfalls

- Trusting the trigger's response body instead of re-reading the object.
- Re-reading as a different identity and conflating a read-permission bug with a write.
- Diffing manually and missing a second field that also changed.

## Done when

- Before and after representations are both saved with their requests.
- The diff lists exactly which fields the trigger changed.

## References

- [OWASP - mass assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [CWE-915 - improperly controlled modification of dynamically-determined object attributes](https://cwe.mitre.org/data/definitions/915.html)

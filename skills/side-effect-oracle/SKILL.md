---
name: side-effect-oracle
description: "Prove the trigger changed server state by observing the effect through a second, independent path instead of trusting the triggering response. Use when the request returns an ambiguous status but is supposed to perform a write, such as a role change or a refund"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, state, verification]
---

# Side Effect Oracle

> Prove the trigger changed server state by observing the effect through a second, independent path instead of trusting the triggering response

**Use when:** the request returns an ambiguous status but is supposed to perform a write, such as a role change or a refund

**Avoid when:** the only observable effect is the response itself and no read path exists

## Procedure

1. Identify a second endpoint that reads the state the trigger is supposed to change.
2. Read it before the trigger and save the representation.
3. Send the trigger and ignore its response body for now.
4. Read the state again through the same second path, as the same identity.
5. Compare the two reads and state which field moved.
6. Use that movement, not the trigger's status code, as the success condition.

## Signals

- The trigger returns 200 but a re-read shows no change.
- A listing endpoint shows the object under the other tenant after the trigger.
- The trigger returns 500 yet the state changed anyway, a partial-success bug.
- The second read is cached and hides the change, which needs a cache-buster.

## Patterns

**1. Observe elsewhere**

```text
trigger: PATCH /users/bob {"role":"owner"} -> 200
read:    GET /team/members as alice -> bob.role == "owner"
```

**2. Assume partial success**

```text
trigger returned 500 but the read shows the role changed  -> effect is real, error is noise
```

**3. Avoid the cache**

```text
second read with Cache-Control: no-cache and a unique query string
```

## Pitfalls

- Trusting the trigger's own success message, which many APIs return optimistically.
- Re-reading through a cached listing and concluding nothing changed.
- Using a third identity to read the state and turning a write bug into a read bug.

## Done when

- A second read path confirms the state change independently of the trigger response.
- The success condition references the field that moved in the second read.

## References

- [OWASP - mass assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [CWE-915 - improperly controlled modification of object attributes](https://cwe.mitre.org/data/definitions/915.html)

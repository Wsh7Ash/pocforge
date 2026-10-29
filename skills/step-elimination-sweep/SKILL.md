---
name: step-elimination-sweep
description: "Delete one step at a time and re-run, keeping only the steps whose removal makes the effect disappear. Use when the PoC grew organically during exploration and now contains setup nobody has questioned"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, method, poc]
---

# Step Elimination Sweep

> Delete one step at a time and re-run, keeping only the steps whose removal makes the effect disappear

**Use when:** the PoC grew organically during exploration and now contains setup nobody has questioned

**Avoid when:** the PoC is already three steps long, where the sweep costs more than it can reveal

## Procedure

1. Number every step in the working PoC and confirm it reproduces end to end.
2. Remove step one and re-run from the remaining steps, recording the outcome.
3. If the effect survives, delete the step permanently and renumber.
4. If the effect disappears, restore the step and mark it as load-bearing.
5. Sweep the rest of the steps one at a time in the same way.
6. Re-run the reduced PoC twice to confirm it still works before publishing it.

## Signals

- A login step is followed by a second login nobody remembers adding.
- The PoC creates a record it never reads.
- An initial enumeration step only exists to find an id you now hard-code as an extract.
- Removing a step changes the response size but not the effect.

## Patterns

**1. Sweep log**

```text
step 2 removed -> effect still present -> deleted
step 4 removed -> effect gone -> load-bearing
```

**2. Renumber after deleting**

```text
keep 1..n contiguous so the report does not reference gaps
```

**3. Confirm the floor**

```text
two consecutive clean runs of the reduced PoC -> ship it
```

## Pitfalls

- Removing two steps at once and losing track of which one carried the effect.
- Deleting a step that only provides authentication, which makes the effect unreachable.
- Publishing a reduced PoC without re-running it, so a broken reduction ships.

## Done when

- Every remaining step is marked load-bearing after a removal test.
- The reduced PoC reproduces twice from a clean state.

## References

- [Wikipedia - delta debugging](https://en.wikipedia.org/wiki/Delta_debugging)
- [OWASP - proof of concept guidance](https://owasp.org/www-project-web-security-testing-guide/)

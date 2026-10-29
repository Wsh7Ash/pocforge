---
name: payload-delta-bisect
description: "Bisect a long payload or path down to the exact substring that triggers the defect, using halves rather than characters. Use when the trigger is a long path, a serialised blob or a template payload where the active part is unknown"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, payload, method]
---

# Payload Delta Bisect

> Bisect a long payload or path down to the exact substring that triggers the defect, using halves rather than characters

**Use when:** the trigger is a long path, a serialised blob or a template payload where the active part is unknown

**Avoid when:** the trigger is a single short value you can already name exactly

## Procedure

1. Save the full working payload and confirm it still triggers the defect.
2. Split the payload in half and test each half separately.
3. Keep the half that still triggers, and discard the other if it does not.
4. Repeat the halving until the payload stops shrinking usefully.
5. Inspect the remaining fragment and name the parser behaviour it exploits.
6. Verify the fragment alone, in the original position, still produces the effect.

## Signals

- Only one half of a traversal path is enough to escape the directory.
- The effect survives with the payload truncated at a parser boundary.
- Encoding a single character differently changes the outcome.
- The minimal fragment is much shorter than the payload you first reported.

## Patterns

**1. Halve, do not guess**

```text
payload: ../../../../etc/passwd
half A: ../../
half B: ../../etc/passwd  -> keep B, repeat
```

**2. Name the parser**

```text
fragment: %2e%2e%2f survives normalisation  -> decode-then-join ordering bug
```

**3. Re-verify in position**

```text
place the fragment back in the original parameter and re-send
```

## Pitfalls

- Bisecting a payload that was URL-encoded twice, so the halves are not equivalent.
- Testing halves in a different parameter and attributing the result to the fragment.
- Stopping at the first short payload without checking the effect class is unchanged.

## Done when

- The minimal fragment is recorded with the parser behaviour it exploits.
- The fragment reproduces the same effect class in its original position.

## References

- [OWASP - path traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22 - improper limitation of a pathname to a restricted directory](https://cwe.mitre.org/data/definitions/22.html)

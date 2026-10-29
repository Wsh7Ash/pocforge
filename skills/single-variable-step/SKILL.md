---
name: single-variable-step
description: "Change exactly one thing per step so that when the response flips, the cause is provable instead of guessed. Use when the trigger requires several edits to a request and it is unclear which edit actually mattered"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, minimize, method]
---

# Single Variable Step

> Change exactly one thing per step so that when the response flips, the cause is provable instead of guessed

**Use when:** the trigger requires several edits to a request and it is unclear which edit actually mattered

**Avoid when:** the defect needs a combination of headers that only works together, in which case vary the set as a unit

## Procedure

1. Write the working trigger as a complete request dump first, with every header you sent.
2. Pick one element to vary: a header, a parameter, a path segment or a body field.
3. Send the request with only that element changed and save both responses.
4. If the response flips, that element is implicated; if not, revert it and pick the next.
5. Repeat until each element in the trigger has a recorded verdict.
6. Rebuild the PoC using only the elements that carried the effect.

## Signals

- Two headers were added at once and the effect appeared.
- Removing a header silently keeps the effect working, which means it was noise.
- A parameter you considered essential turns out to change nothing.
- The effect persists with the body removed entirely.

## Patterns

**1. One element per row**

```text
row a: baseline -> 403
row b: +X-Original-URL -> 200  <- effect
row c: +X-Rewrite-URL only -> 403
```

**2. Hold everything else byte-identical**

```text
diff only the changed header;
keep method, path, body length and cookie constant
```

**3. Rebuild from survivors**

```text
survivors: X-Original-URL
noise: X-Forwarded-For, Accept-Language  -> drop the noise from the PoC
```

## Pitfalls

- Changing headers and parameters together and then attributing the effect to the wrong one.
- Keeping decorative headers in the final PoC, which makes triage wonder what is load-bearing.
- Assuming the last change caused the effect when an earlier one had already flipped it.

## Done when

- Each element of the trigger has a recorded keep or drop verdict.
- The final PoC contains only elements shown to be necessary.

## References

- [PortSwigger - bypassing access controls with headers](https://portswigger.net/web-security/access-control)
- [RFC 9110 - header field semantics](https://www.rfc-editor.org/rfc/rfc9110.html#section-5.3)

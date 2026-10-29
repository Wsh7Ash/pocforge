---
name: deterministic-seed-pinning
description: "Pin every source of randomness, clock value and generated identifier the PoC depends on, so a re-run produces the same decision rather than a similar one. Use when the trigger involves tokens, nonces, generated ids, timestamps or randomised ordering"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, determinism, method]
---

# Deterministic Seed Pinning

> Pin every source of randomness, clock value and generated identifier the PoC depends on, so a re-run produces the same decision rather than a similar one

**Use when:** the trigger involves tokens, nonces, generated ids, timestamps or randomised ordering

**Avoid when:** the effect is independent of any generated value and the request is fully static

## Procedure

1. List every value in the request that the server or a prior step generated.
2. Decide which of those values the trigger actually depends on.
3. Capture those values from the run and store them as named extracts.
4. Replace literals in the request with references to the extracts.
5. Set any client-side clock or random seed explicitly where the tool allows it.
6. Re-run twice from the same extracts and confirm identical outcomes.

## Signals

- The trigger fails when a nonce or timestamp is reused from a previous run.
- Ids differ between runs but the effect does not, so the id is not load-bearing.
- A one-second window decides success, which needs its own timing skill.
- A token expires mid-run and the later steps fail for the wrong reason.

## Patterns

**1. Extract, then reference**

```text
step 1 returns {"id": 1042} -> extract order_id
step 3 uses /orders/{{order_id}}  -> no hand-copied ids
```

**2. Pin the clock where possible**

```text
created_after=2026-10-29T00:00:00Z  -> avoid "now" so the diff is stable
```

**3. Two runs, one result**

```text
run A: 200, 812 bytes
run B: 200, 812 bytes  -> deterministic; report it that way
```

## Pitfalls

- Hard-coding an id from an earlier session that no longer exists on the target.
- Reusing a nonce that the server has already seen, which turns a valid trigger into a rejected one.
- Calling a flaky trigger deterministic without running it twice.

## Done when

- Every generated value used by the trigger is extracted rather than typed.
- Two consecutive runs produce the same status and effect.

## References

- [RFC 6750 - bearer token usage](https://www.rfc-editor.org/rfc/rfc6750.html)
- [OWASP - testing for session management](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/)

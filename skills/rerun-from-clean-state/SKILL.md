---
name: rerun-from-clean-state
description: "Replay the finished PoC from a fresh session and unmodified baseline, because half of all failed reproductions are caused by leftover state from the successful run. Use when the PoC mutated data, created sessions or consumed a one-time token during exploration"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, reproduce, state]
---

# Rerun From Clean State

> Replay the finished PoC from a fresh session and unmodified baseline, because half of all failed reproductions are caused by leftover state from the successful run

**Use when:** the PoC mutated data, created sessions or consumed a one-time token during exploration

**Avoid when:** the effect is genuinely one-shot per account and you have documented that limitation

## Procedure

1. Discard cookies, tokens and cached responses from the exploration session.
2. Create fresh identities and seed records exactly as the preconditions describe.
3. Run the PoC steps in order without editing anything mid-run.
4. Compare the final response with the one you originally captured.
5. If the run diverges, fix the spec rather than the run and start again.
6. Record the clean run as the canonical evidence file for submission.

## Signals

- The second run fails because a token was already redeemed.
- The object created in the first run already exists, so a create step now returns 409.
- A cached response hides the effect on the second run.
- The clean run needs an extra step your original narrative omitted.

## Patterns

**1. Reset everything**

```text
new cookie jar, new tokens, new seed records, empty cache  -> then run
```

**2. Canonical evidence**

```text
results/clean-run-2026-10-29.http  -> the file the report cites
```

**3. Fix the spec, not the run**

```text
if a step needed a manual fix, add that step to the spec and rerun
```

## Pitfalls

- Reusing the session where the bug was found and calling the run clean.
- Patching the run by hand and not reflecting the fix back into the documented steps.
- Skipping the rerun because the first attempt was convincing.

## Done when

- A fresh session reproduces the effect using only documented steps.
- The canonical run is saved and cited by the report.

## References

- [OWASP - testing checklist](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - report reproduction guidance](https://docs.hackerone.com/en/articles/8475114-scope)

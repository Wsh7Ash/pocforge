---
name: oracle-nondeterminism-budget
description: "Quantify how often a trigger must be retried before it fires, so an intermittent result is reported as a rate rather than as a certainty. Use when the trigger involves caching, background jobs, race windows or eventual consistency"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, determinism, triage]
---

# Oracle Nondeterminism Budget

> Quantify how often a trigger must be retried before it fires, so an intermittent result is reported as a rate rather than as a certainty

**Use when:** the trigger involves caching, background jobs, race windows or eventual consistency

**Avoid when:** the effect is immediate and reproducible on every attempt

## Procedure

1. Run the trigger ten times from a clean equivalent state and count successes.
2. Identify what varies between a success and a failure, such as cache warmth or job timing.
3. Remove that variation where possible by forcing a cache miss or waiting for the job.
4. Re-run ten times with the variation controlled and record the new rate.
5. Report both rates so triage knows the difficulty of reproduction.
6. If the rate stays low, describe the retry loop in the PoC instead of hiding it.

## Signals

- First attempt after a deploy succeeds and later attempts fail.
- Success correlates with a cache miss or a cold connection.
- A background job completes between attempts and changes the outcome.
- Success rate improves markedly once a wait is added.

## Patterns

**1. Rate before and after**

```text
uncontrolled: 3/10
cache-busted: 9/10  -> report both
```

**2. Name the varying factor**

```text
success only when the object is not in the read cache  -> cache-buster in step 2
```

**3. Script the retry**

```text
for i in 1..10; do trigger && break; done  -> bounded, documented retries
```

## Pitfalls

- Reporting the one successful attempt out of twenty as a deterministic repro.
- Retrying hundreds of times against a live target and tripping rate limits or abuse detection.
- Averaging away a real difference by mixing controlled and uncontrolled runs.

## Done when

- A measured success rate is recorded for both controlled and uncontrolled runs.
- The PoC either removes the variation or documents the retry loop.

## References

- [PortSwigger - race conditions](https://portswigger.net/web-security/race-conditions)
- [OWASP - business logic testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)

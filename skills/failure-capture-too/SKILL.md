---
name: failure-capture-too
description: "Save the runs where the trigger did not work, because a documented non-reproduction is what turns an anecdote into a bounded, credible claim. Use when the trigger is intermittent or configuration dependent and the writeup will otherwise look selective"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, evidence, honesty]
---

# Failure Capture Too

> Save the runs where the trigger did not work, because a documented non-reproduction is what turns an anecdote into a bounded, credible claim

**Use when:** the trigger is intermittent or configuration dependent and the writeup will otherwise look selective

**Avoid when:** the trigger reproduced cleanly every time and there is no failed attempt worth reporting

## Procedure

1. Keep a log of every attempt, with the configuration and the outcome.
2. Save the response of at least one failed attempt next to the successful ones.
3. Work out which element differed between the failed and successful attempts.
4. State that difference as a bound in the report, such as requires a fresh session.
5. Attach the failed attempt to the evidence set with a clear label.
6. Re-read the impact claim and narrow it to the configurations that actually worked.

## Signals

- The successful attempt used a fresh session while failures reused one.
- Failures cluster on a particular client version or region.
- A failed attempt returned a different error than expected, hinting at a second gate.
- You cannot explain why an attempt failed, which means the oracle is not understood yet.

## Patterns

**1. Label the attempt**

```text
attempt 3: fresh session, 5 ms delay -> effect
attempt 4: reused session, 5 ms delay -> no effect  -> session freshness matters
```

**2. Bound with the failure**

```text
reproduces only on a session that has not yet read the object  -> say so in the spec
```

**3. Keep the log**

```text
results/attempts.log with one line per attempt: config, status, effect yes or no
```

## Pitfalls

- Deleting failed attempts so the writeup looks cleaner and the bound is lost.
- Reporting a one-hundred-percent success rate that a triager will immediately contradict.
- Ignoring an unexplained failure that actually points at a second precondition.

## Done when

- At least one failed attempt is saved and explained in the spec.
- The impact claim is bounded by the differences the failures revealed.

## References

- [HackerOne - report quality guidance](https://docs.hackerone.com/en/articles/8475114-scope)
- [OWASP - testing for business logic](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)

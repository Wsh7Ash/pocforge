---
name: timing-window-recording
description: "Record the time window a race or expiry-dependent trigger needs, with measured timings rather than an assumption that the window is wide. Use when the defect only fires inside a narrow interval, such as a race between check and use or a token that expires mid-flow"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, race, timing]
---

# Timing Window Recording

> Record the time window a race or expiry-dependent trigger needs, with measured timings rather than an assumption that the window is wide

**Use when:** the defect only fires inside a narrow interval, such as a race between check and use or a token that expires mid-flow

**Avoid when:** the trigger has no timing dimension and both requests can be sent minutes apart

## Procedure

1. Measure the baseline latency of each request in the pair across several samples.
2. Estimate the window from the difference between the check and the use.
3. Send the pair with a deliberate delay first, and confirm the effect does not appear.
4. Reduce the delay step by step and record the point where the effect starts.
5. Repeat the successful configuration several times and report the success rate.
6. State the window and the success rate in the spec, not just the winning attempt.

## Signals

- The effect only appears when both requests land in the same millisecond range.
- Success rate is well below one hundred percent across attempts.
- A single retry makes the effect vanish, suggesting the first request already consumed state.
- The window is wider on a slow endpoint, which makes reproduction easier to describe.

## Patterns

**1. Measure, then narrow**

```text
baseline latency: 42 ms median
delay 200 ms -> no effect
delay 5 ms  -> effect in 6 of 10 attempts
```

**2. Report the rate**

```text
trigger: 2 parallel POST /redeem with the same code
result: 6/10 attempts credited twice  -> state the rate
```

**3. Describe the pair as one unit**

```text
step 3: send both requests concurrently, do not wait for the first response
```

## Pitfalls

- Reporting a single lucky attempt as a reliable race without a success rate.
- Measuring latency from a laptop on a different continent than the target and generalising.
- Widening the window with extra requests and calling the resulting state corruption a race.

## Done when

- The spec states the measured window and the observed success rate.
- At least one configuration is shown to fail, bounding the window from above.

## References

- [PortSwigger - race conditions](https://portswigger.net/web-security/race-conditions)
- [CWE-362 - concurrent execution using shared resource with improper synchronization](https://cwe.mitre.org/data/definitions/362.html)

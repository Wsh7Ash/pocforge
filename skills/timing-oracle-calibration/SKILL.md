---
name: timing-oracle-calibration
description: "Calibrate a timing signal against repeated baselines before claiming it, because a single slow response is not evidence of a blind extraction channel. Use when the only observable difference between a hit and a miss is how long the server takes"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, timing, blind]
---

# Timing Oracle Calibration

> Calibrate a timing signal against repeated baselines before claiming it, because a single slow response is not evidence of a blind extraction channel

**Use when:** the only observable difference between a hit and a miss is how long the server takes

**Avoid when:** a status code, body difference or side effect already distinguishes the cases

## Procedure

1. Send the negative case twenty times and record the full distribution, not the mean.
2. Send the positive case twenty times and record the same distribution.
3. Compare medians and confirm the distributions do not overlap.
4. Increase the injected delay in the payload until separation is unambiguous.
5. Repeat the measurement at a different time of day to check stability.
6. Report the medians, the sample size and the overlap, never a single timing.

## Signals

- Median difference exceeds the spread of both samples by a wide margin.
- A single run shows a huge difference that disappears on repetition.
- Network jitter dominates the signal, making the channel unusable.
- The delay scales with the number of matched rows, confirming a data-dependent branch.

## Patterns

**1. Distribution, not mean**

```text
negative: median 412 ms, p95 480 ms
positive: median 3120 ms, p95 3290 ms  -> separated
```

**2. Scale the delay**

```text
inject sleep 3s on match  -> signal far above jitter
```

**3. Report the caveat**

```text
single-region measurement, 20 samples each, no overlap observed
```

## Pitfalls

- Reporting one slow response as a blind injection channel without a sample.
- Measuring from a connection that reuses a cold TLS session on the first request only.
- Ignoring that a WAF delay can produce the same separation for the wrong reason.

## Done when

- Both distributions are recorded with sample sizes and medians.
- The claim states the separation and any measurement caveats.

## References

- [PortSwigger - blind SQL injection](https://portswigger.net/web-security/sql-injection/blind)
- [OWASP - blind injection techniques](https://owasp.org/www-community/attacks/Blind_SQL_Injection)

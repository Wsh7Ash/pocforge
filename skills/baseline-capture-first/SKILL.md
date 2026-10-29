---
name: baseline-capture-first
description: "Capture a clean baseline response before touching anything, so every later difference has something honest to be compared against. Use when starting any PoC whose claim depends on a response differing from normal behaviour"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, oracle, evidence]
---

# Baseline Capture First

> Capture a clean baseline response before touching anything, so every later difference has something honest to be compared against

**Use when:** starting any PoC whose claim depends on a response differing from normal behaviour

**Avoid when:** the effect is a crash or a hard error that is unambiguous without a comparison

## Procedure

1. Send the request in its normal, intended form as the intended identity.
2. Save the full response bytes, including status line and headers, not just the body.
3. Record the exact request that produced it, with all headers you sent.
4. Repeat the baseline twice and confirm both responses are equivalent.
5. Only then introduce the variable that is supposed to change the outcome.
6. Keep the baseline file in the evidence set and cite it from the oracle.

## Signals

- Your first attempt at the trigger already returned the same body as the baseline.
- The baseline differs between two consecutive sends, which means the oracle is unstable.
- A cache header on the baseline explains a later difference.
- The baseline is an error page you did not notice.

## Patterns

**1. Byte-level baseline**

```text
GET /orders/1042 as alice -> 200, 812 bytes, ETag: "a1b2"
save: results/baseline-alice-order.http
```

**2. Baseline twice**

```text
send 2x, diff the two files  -> identical means the endpoint is deterministic
```

**3. Cite the baseline from the oracle**

```text
oracle.success: step 4 body equals baseline except order_id
oracle.failure: step 4 returns 403 like the control
```

## Pitfalls

- Comparing against a remembered response instead of a saved one.
- Capturing only the JSON body and losing the status code that carries the real signal.
- Taking a baseline while an unrelated feature flag or cache state was different.

## Done when

- A saved baseline request and response exist in the evidence set.
- The baseline was captured twice and shown to be stable.

## References

- [OWASP WSTG - testing for error handling](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/)
- [RFC 9110 - HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html)

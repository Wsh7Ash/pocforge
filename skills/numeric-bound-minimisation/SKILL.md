---
name: numeric-bound-minimisation
description: "Replace large or awkward numbers with the smallest value that still triggers, which turns a vague quantity bug into a stated missing bound. Use when the trigger uses a big quantity, a negative amount, a zero price or an overflowing counter"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, business-logic, bounds]
---

# Numeric Bound Minimisation

> Replace large or awkward numbers with the smallest value that still triggers, which turns a vague quantity bug into a stated missing bound

**Use when:** the trigger uses a big quantity, a negative amount, a zero price or an overflowing counter

**Avoid when:** the defect is structural and the numeric value is irrelevant to whether it fires

## Procedure

1. Record the value you used when the defect first appeared.
2. Halve it repeatedly until the defect stops firing, then bisect between the last two values.
3. Try zero and negative one, since missing lower bounds are a separate defect class.
4. Try the maximum the field accepts and note whether the server clamps or errors.
5. State the smallest accepted value that produces the effect as the boundary.
6. Describe the missing validation in one sentence using the observed boundary.

## Signals

- A negative quantity is accepted and increases a balance.
- Zero passes validation and creates a free order.
- A very large value is accepted without a clamp, hinting at an overflow.
- The error for the maximum value reveals the column width or type.

## Patterns

**1. Bisect to the boundary**

```text
qty 100 -> refund doubled
qty 10  -> refund doubled
qty 2   -> refund doubled
qty 1   -> normal  -> boundary is 2
```

**2. Probe the other side**

```text
qty -1 -> accepted, balance increased  -> missing lower bound
```

**3. State the missing check**

```text
no validation that qty > 0 and qty <= stock  -> two defects, one request
```

## Pitfalls

- Reporting a huge number as the trigger when the same effect fires at two.
- Missing the negative-value case because you only tested upward from one.
- Calling an accepted large value a crash without checking whether the response was clamped.

## Done when

- The smallest triggering value is recorded with the value that fails just below it.
- The missing validation is described in terms of the observed boundary.

## References

- [OWASP - business logic testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)
- [CWE-840 - business logic errors](https://cwe.mitre.org/data/definitions/840.html)

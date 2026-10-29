---
name: blast-radius-statement
description: "Quantify how much data or functionality the defect exposes, using counts you actually observed rather than adjectives about severity. Use when the impact section needs a number that a triager can sanity-check, such as how many records or tenants are reachable"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [impact, frame, triage]
---

# Blast Radius Statement

> Quantify how much data or functionality the defect exposes, using counts you actually observed rather than adjectives about severity

**Use when:** the impact section needs a number that a triager can sanity-check, such as how many records or tenants are reachable

**Avoid when:** the effect is binary, like an authentication bypass on a single admin account

## Procedure

1. Identify the unit of exposure: records, tenants, users, files or transactions.
2. Count what you reached with the PoC using the smallest representative sample.
3. State how you estimated the total, for example by checking whether ids are sequential.
4. Bound the claim to what the sample proves rather than extrapolating silently.
5. Note the data classification of the exposed fields, such as PII or payment metadata.
6. Put the count and the bound in one sentence in the impact section.

## Signals

- Ids are sequential or timestamps, which makes enumeration plausible but unproven.
- The response includes fields belonging to a different tenant or user.
- A count endpoint returns a total far larger than your sample.
- The exposed field appears in the product's data-classification documentation.

## Patterns

**1. Sample then bound**

```text
reached: 3 of 3 sampled ids across 2 tenants
bound: at least 2 tenants, enumeration unproven  -> do not claim all
```

**2. Name the exposed field**

```text
response fields: email, phone, last4  -> PII plus payment metadata, not just "user data"
```

**3. Count with one request when available**

```text
GET /admin/stats -> {"orders": 481203}  -> exposure ceiling, cite it as context
```

## Pitfalls

- Multiplying a sample by a guessed total and presenting it as measured impact.
- Calling a response critical without naming a single sensitive field it contained.
- Ignoring that the same data is public elsewhere, which collapses the impact claim.

## Done when

- The impact section contains a count that came from an actual response.
- The bound on extrapolation is stated next to the count.

## References

- [OWASP - sensitive data exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)
- [Bugcrowd - vulnerability rating taxonomy](https://bugcrowd.com/vulnerability-rating-taxonomy)

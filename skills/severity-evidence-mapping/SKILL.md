---
name: severity-evidence-mapping
description: "Tie the claimed severity to specific evidence lines so a downgrade requires contradicting a request rather than arguing about wording. Use when the program uses a fixed severity taxonomy and you want the rating to survive triage without a negotiation cycle"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [impact, triage, severity]
---

# Severity Evidence Mapping

> Tie the claimed severity to specific evidence lines so a downgrade requires contradicting a request rather than arguing about wording

**Use when:** the program uses a fixed severity taxonomy and you want the rating to survive triage without a negotiation cycle

**Avoid when:** the program has no taxonomy and asks researchers to describe impact in prose only

## Procedure

1. Read the program's severity taxonomy and pick the row that matches your observed effect.
2. Quote the row's criteria in the spec next to the matching evidence reference.
3. Map each criterion to a step number that demonstrated it.
4. Remove criteria you cannot map to a step, and lower the claim to what remains.
5. Check whether the program caps severity for a bug class regardless of impact.
6. Record the mapping in a small table in the report appendix.

## Signals

- The taxonomy row requires proof of cross-tenant access and your steps stop at your own tenant.
- The program caps authorization findings at medium without a demonstrated data breach.
- Your evidence supports confidentiality but you claimed integrity as well.
- The rating depends on an unauthenticated attacker while your steps use an admin token.

## Patterns

**1. Criterion to step map**

```text
criteria: cross-tenant read of PII
evidence: step 3 (bob reads alice's order), field email present  -> high
```

**2. Drop what is not shown**

```text
claimed: read and modify
shown: read only  -> remove the modify clause before submitting
```

**3. Respect the class cap**

```text
program note: IDOR without sensitive data caps at medium  -> claim medium, not high
```

## Pitfalls

- Claiming the highest row of the taxonomy while demonstrating a lower row's evidence.
- Ignoring a documented class cap, which reads as unfamiliarity with the program.
- Mapping criteria to prose paragraphs instead of to reproducible step numbers.

## Done when

- Every claimed criterion maps to a numbered step and an evidence file.
- The final severity matches the taxonomy row the evidence actually satisfies.

## References

- [Bugcrowd - vulnerability rating taxonomy](https://bugcrowd.com/vulnerability-rating-taxonomy)
- [CVSS v3.1 specification](https://www.first.org/cvss/v3-1/specification-document)

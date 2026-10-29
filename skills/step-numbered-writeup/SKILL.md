---
name: step-numbered-writeup
description: "Number every action so the report, the evidence files and the retest all refer to the same steps by the same numbers. Use when the report has more than three actions or cites evidence files per action"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, writing, triage]
---

# Step Numbered Writeup

> Number every action so the report, the evidence files and the retest all refer to the same steps by the same numbers

**Use when:** the report has more than three actions or cites evidence files per action

**Avoid when:** the whole report is one request, where numbering adds ceremony

## Procedure

1. Write the steps as imperative actions in the order a reader must perform them.
2. Give each step a number and keep the numbering stable through edits.
3. Attach the request and response file for each step beside the number.
4. Reference steps by number in the impact and oracle sections.
5. Remove any narrative that is not a step or a claim.
6. Read the report top to bottom and check every step number resolves.

## Signals

- The impact section mentions a behaviour no step performs.
- Two steps share a number after an edit.
- An evidence file is not referenced by any step.
- A step describes an assumption rather than an action.

## Patterns

**1. Stable numbering**

```text
3. bob GET /orders/{{order_id}} -> 200, alice's order
   evidence: results/step-03.http
```

**2. Cross-reference**

```text
oracle.success refers to step 3
impact refers to steps 3 and 4
```

**3. One action per step**

```text
bad: log in and then read the order
good: 1. authenticate as alice  2. read the order
```

## Pitfalls

- Editing the steps and leaving the impact section pointing at old numbers.
- Combining setup and trigger into one step so the reader cannot see the boundary.
- Describing intent instead of action, which a triager cannot replay.

## Done when

- Every claim and evidence file resolves to a numbered step.
- Each step is a single replayable action.

## References

- [HackerOne - report writing guidance](https://docs.hackerone.com/en/articles/8475114-scope)
- [OWASP - reporting template](https://owasp.org/www-project-web-security-testing-guide/)

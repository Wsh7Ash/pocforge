---
name: impact-first-summary
description: "Open with the one sentence a triager will quote internally, naming what was exposed, to whom and under which condition. Use when the report summary currently describes the technical mechanism instead of the consequence"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, writing, impact]
---

# Impact First Summary

> Open with the one sentence a triager will quote internally, naming what was exposed, to whom and under which condition

**Use when:** the report summary currently describes the technical mechanism instead of the consequence

**Avoid when:** the program's template already enforces a structured impact field

## Procedure

1. Write the exposure in one sentence: what data or capability, for which population.
2. Move the mechanism to the second sentence, after the consequence.
3. Name the preconditions in a short clause rather than burying them later.
4. Delete adjectives such as critical, severe and devastating from the summary.
5. Read it back as if quoting it in a status meeting and check it still means something.
6. Put the same sentence at the top of the report and in the impact section.

## Signals

- The summary starts with the endpoint name rather than the consequence.
- A reader cannot tell from the summary whether data was exposed or modified.
- The summary claims a mechanism you have not demonstrated.
- The severity word in the summary has no supporting number.

## Patterns

**1. Consequence first**

```text
Any authenticated member of a tenant can read another tenant's order records, including customer email and phone, by changing the order id.
```

**2. Mechanism second**

```text
The item route performs no ownership check before serialising the order.
```

**3. No adjectives**

```text
delete: critical, severe, devastating, complete takeover  -> keep the count and the field names
```

## Pitfalls

- Leading with the bug class, which tells triage nothing about consequences.
- Writing a summary so long that the consequence is in the third paragraph.
- Claiming complete takeover in the first line when the steps show a read.

## Done when

- The first sentence names the exposed data and the affected population.
- The summary contains no severity adjective without an accompanying number.

## References

- [HackerOne - report quality](https://docs.hackerone.com/en/articles/8475114-scope)
- [Bugcrowd - writing submissions](https://docs.bugcrowd.com/researchers/reporting-managing-submissions/)

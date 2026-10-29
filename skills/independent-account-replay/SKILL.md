---
name: independent-account-replay
description: "Hand the PoC to a second researcher or a second account set and see whether it reproduces without your explanation. Use when the PoC relies on implied knowledge, such as knowing where a value appears in the UI"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, reproduce, review]
---

# Independent Account Replay

> Hand the PoC to a second researcher or a second account set and see whether it reproduces without your explanation

**Use when:** the PoC relies on implied knowledge, such as knowing where a value appears in the UI

**Avoid when:** the PoC is fully scripted and already runs from a single command with no human steps

## Procedure

1. Give the spec and repository to someone who has not seen the target, with no verbal hints.
2. Ask them to run the reproduction command and report the observed status.
3. Record where they got stuck, since each stop is a documentation defect.
4. Add the missing precondition or step they needed, and remove any step they found confusing.
5. Have them re-run after the edits and confirm they reach the effect unaided.
6. Keep their run output as a second canonical evidence file.

## Signals

- The reviewer asks where a token or id comes from.
- They run the steps but hit a login wall your account had already passed.
- They interpret an expected result differently than you did.
- Their run succeeds but produces a different response shape, hinting at variance.

## Patterns

**1. Silent handoff**

```text
give: README, spec, repro command
withhold: any explanation  -> every question is a doc bug
```

**2. Log the stops**

```text
stop 1: did not know how to obtain ALICE_TOKEN
stop 2: assumed order_id was literal
```

**3. Second canonical run**

```text
results/independent-run.http  -> someone else's bytes, same effect
```

## Pitfalls

- Standing over the reviewer and answering questions, which defeats the test.
- Giving a modified spec that only works on your branch of the repository.
- Treating a successful run as proof the docs were clear when they asked three questions.

## Done when

- A second person reaches the effect using only the published artifacts.
- Every stop they hit has been fixed in the spec or README.

## References

- [OWASP - reporting standards](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - report writing](https://docs.hackerone.com/en/articles/8475114-scope)

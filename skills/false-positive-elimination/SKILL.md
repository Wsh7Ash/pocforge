---
name: false-positive-elimination
description: "Actively try to explain away your own finding with benign causes, and only submit once each explanation has a request that rules it out. Use when the effect could plausibly be caused by caching, a shared grant, a demo account or a client-side check"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, false-positive, triage]
---

# False Positive Elimination

> Actively try to explain away your own finding with benign causes, and only submit once each explanation has a request that rules it out

**Use when:** the effect could plausibly be caused by caching, a shared grant, a demo account or a client-side check

**Avoid when:** the effect is a hard server-side disclosure that no benign configuration could produce

## Procedure

1. Write down the three most likely benign explanations for the effect.
2. Design one request or configuration change that would confirm each explanation.
3. Run them and record the outcome, including ones you cannot fully rule out.
4. If any benign explanation survives, downgrade or withdraw the finding.
5. State in the report which alternatives were tested and eliminated.
6. Keep the elimination requests as evidence alongside the trigger.

## Signals

- The object is readable by a team-wide role you had not checked.
- A demo tenant has relaxed rules that your test account inherited.
- The check happens in the client, so a direct request behaves differently than expected.
- A shared link with a token makes the object public by design.

## Patterns

**1. Three alternatives**

```text
1. shared team grant -> checked /team/members, bob not a member
2. demo tenant -> alice is on plan pro, not demo
3. public link -> order has no share token
```

**2. Test the client-only theory**

```text
send the request without the UI -> still 200  -> server-side, not client-side
```

**3. Record the survivors**

```text
could not rule out: an internal support role  -> note it, do not hide it
```

## Pitfalls

- Skipping the alternative check because the finding feels obvious.
- Ruling out an alternative with a request that does not actually test it.
- Withdrawing a real finding because an unrelated benign cause was also present.

## Done when

- Each plausible benign cause has a recorded test and outcome.
- The report lists the alternatives that were eliminated.

## References

- [OWASP - false positive handling](https://owasp.org/www-project-web-security-testing-guide/)
- [Bugcrowd - valid submission criteria](https://docs.bugcrowd.com/researchers/reporting-managing-submissions/)

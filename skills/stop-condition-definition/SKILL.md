---
name: stop-condition-definition
description: "Write down in advance the point at which the PoC stops touching production, so exploration cannot drift into destructive testing without a decision. Use when the test path passes near delete, refund, invite, payment or bulk-export functionality"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [safety, frame, scope]
---

# Stop Condition Definition

> Write down in advance the point at which the PoC stops touching production, so exploration cannot drift into destructive testing without a decision

**Use when:** the test path passes near delete, refund, invite, payment or bulk-export functionality

**Avoid when:** the whole PoC is read-only against synthetic data you created yourself

## Procedure

1. List the operations in the test path that change state or notify a real person.
2. Mark which of those you may perform on your own test data and which you may not.
3. Define the stop condition as a sentence, such as stop before any request that emails a non-test address.
4. Prefer your own tenant, your own records and your own recipient addresses for every mutating step.
5. Record the stop condition in the spec so it is visible to anyone replaying the PoC.
6. When the only path to proof crosses the line, write the PoC up to the boundary and say so.

## Signals

- The next step would send a real email, SMS or push notification to a third party.
- The next step deletes or refunds an object you do not own.
- The trigger requires brute force against another tenant's identifiers.
- The program's rules prohibit automated scanning or high-volume requests.

## Patterns

**1. Boundary in the spec**

```text
stop_condition: no request may target a record, address or account not created by this PoC
```

**2. Substitute your own recipient**

```text
before: invite victim@customer.example
allowed: invite poc+1@your-own-domain  -> same code path, no third party
```

**3. Prove up to the boundary**

```text
step 5 returns the victim's email in the preview response  -> effect shown without sending anything
```

## Pitfalls

- Testing a destructive path on a real customer record because it was the only accessible id.
- Sending notifications to addresses you do not control and calling it harmless.
- Deciding the boundary mid-test, when the interesting response is already one request away.

## Done when

- The spec states a stop condition that a reader can apply without judgement calls.
- Every mutating step targets data the PoC itself created.

## References

- [HackerOne - researcher ethics and safe testing](https://docs.hackerone.com/en/articles/8475114-scope)
- [OWASP - testing guide introduction](https://owasp.org/www-project-web-security-testing-guide/)

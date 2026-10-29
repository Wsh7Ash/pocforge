---
name: claim-versus-effect-separation
description: "Split the PoC into the effect you observed and the claim you are making about it, then prove only the effect and label the rest as inference. Use when the observed response is weaker than the impact you want to claim, which is the most common reason a valid bug gets downgraded"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [triage, frame, impact]
---

# Claim Versus Effect Separation

> Split the PoC into the effect you observed and the claim you are making about it, then prove only the effect and label the rest as inference

**Use when:** the observed response is weaker than the impact you want to claim, which is the most common reason a valid bug gets downgraded

**Avoid when:** the effect is already the full impact, such as reading another tenant's record in the response body

## Procedure

1. Write one sentence describing exactly what the server did, with no adjectives.
2. Write a separate sentence for what that behaviour implies an attacker could do.
3. Check whether your steps demonstrate the second sentence or only the first.
4. If only the first is demonstrated, retitle the report after the effect and mark the rest as inference.
5. Where the inference is checkable with one more request, add that request as a step.
6. Keep both sentences visible in the final writeup so triage can follow your reasoning.

## Signals

- The word could appears more often than a status code in your summary.
- The impact section describes data you never saw in a response.
- Your steps end at an error message rather than at another user's data.
- A triager would need a second vulnerability to reach the claimed impact.

## Patterns

**1. Effect, then inference**

```text
effect: GET /orders/1042 as bob returns alice's order JSON (200)
inference: order ids are sequential, so any order is readable  -> untested
```

**2. Promote inference only with a step**

```text
step 4 repeats with id 1043 and returns a different tenant's order  -> inference is now an effect
```

**3. Retitle to the effect**

```text
before: full account takeover via IDOR
after: cross-tenant read of order records (IDOR)
```

## Pitfalls

- Chaining two unproven assumptions into a critical rating that triage will reject outright.
- Describing what an attacker could do when the response body already shows what they did.
- Hiding the gap between effect and claim, which reads as inflation rather than confidence.

## Done when

- The summary states the observed effect without adjectives.
- Every inference is labelled and, where possible, promoted to its own step.

## References

- [OWASP - insecure direct object reference](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)
- [CWE-639 - authorization bypass through user-controlled key](https://cwe.mitre.org/data/definitions/639.html)

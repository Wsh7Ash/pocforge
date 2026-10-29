---
name: minimal-account-pair-setup
description: "Stand up the smallest pair of accounts that can demonstrate the difference, and script their creation so the PoC does not depend on your long-lived test users. Use when the effect only appears between two specific real accounts whose history you no longer remember"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, setup, authz]
---

# Minimal Account Pair Setup

> Stand up the smallest pair of accounts that can demonstrate the difference, and script their creation so the PoC does not depend on your long-lived test users

**Use when:** the effect only appears between two specific real accounts whose history you no longer remember

**Avoid when:** the program forbids creating additional accounts, in which case document the constraint and use provided test identities

## Procedure

1. Create two fresh accounts with the minimum roles the trigger needs.
2. Record the signup path, required fields and any invite step as numbered preconditions.
3. Give both accounts a predictable label and store their tokens in environment variables.
4. Re-run the trigger with the fresh pair and confirm the effect still appears.
5. Delete or disable the accounts after the test, and note that in cleanup.
6. Document any limit the program imposes on account creation.

## Signals

- The effect disappears with fresh accounts, which points at accumulated state.
- Signup requires an invite, making the pair itself a precondition a triager must reproduce.
- One account's role was granted manually by support weeks ago.
- A fresh account hits a different onboarding flow than your main account.

## Patterns

**1. Two accounts, two tokens**

```text
signup alice -> ALICE_TOKEN
signup bob   -> BOB_TOKEN
trigger uses only these two
```

**2. Script the setup**

```text
precondition 1: POST /signup {email: poc+a@example.test}
precondition 2: verify via the program's test mailbox
```

**3. Prove it is not accumulated state**

```text
fresh pair reproduces -> the defect is not a stale-data artifact
```

## Pitfalls

- Relying on a test account that support manually promoted, which triage cannot recreate.
- Creating accounts with real email addresses and leaving them live after testing.
- Forgetting that a fresh account may not have the feature flag the trigger needs.

## Done when

- The effect reproduces with accounts created by the documented preconditions.
- Both accounts are removed or disabled as part of cleanup.

## References

- [OWASP WSTG - testing for authorization](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/)
- [PortSwigger - testing access control with multiple accounts](https://portswigger.net/web-security/access-control)

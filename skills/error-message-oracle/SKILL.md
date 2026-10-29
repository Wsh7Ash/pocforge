---
name: error-message-oracle
description: "Turn differential error text into a reliable oracle, while checking that the difference reveals the bug rather than just the framework. Use when the endpoint returns distinct errors for existing and non-existing objects, or for parsed and unparsed input"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [oracle, enumeration, errors]
---

# Error Message Oracle

> Turn differential error text into a reliable oracle, while checking that the difference reveals the bug rather than just the framework

**Use when:** the endpoint returns distinct errors for existing and non-existing objects, or for parsed and unparsed input

**Avoid when:** errors are generic and identical across all cases, which means there is no channel here

## Procedure

1. Send a request with a known-valid identifier and record the exact error or success text.
2. Send the same request with a known-invalid identifier and record that text.
3. Diff the two and identify the smallest stable distinguishing substring.
4. Repeat each case three times to confirm the strings do not vary with request id.
5. Use the substring, not the whole message, as the oracle condition.
6. Check whether the same distinction is available through response length or status instead.

## Signals

- Not found versus forbidden wording reveals whether an object exists.
- A stack trace names the database driver or ORM version.
- The error includes the raw input, which is a reflected injection point.
- A validation error lists accepted fields, disclosing the schema.

## Patterns

**1. Stable substring**

```text
existing:  "order 1042 not visible to this account"
missing:   "order not found"  -> distinguishes existence
```

**2. Confirm stability**

```text
repeat 3x, same substring, different request_id  -> safe to key on
```

**3. Prefer the coarser channel**

```text
same distinction visible as 404 vs 403  -> use status, it is harder to break
```

## Pitfalls

- Keying on a full message that includes a request id and differs on every call.
- Treating a framework default 404 page as evidence of an application-level check.
- Reporting stack traces as high severity without showing what they disclose.

## Done when

- The oracle uses a substring shown to be stable across repeated calls.
- The report states what the error difference discloses about server state.

## References

- [CWE-209 - generation of error message containing sensitive information](https://cwe.mitre.org/data/definitions/209.html)
- [OWASP - error handling cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

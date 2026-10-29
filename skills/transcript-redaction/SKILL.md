---
name: transcript-redaction
description: "Redact credentials and third-party personal data from transcripts without destroying the evidence the triager needs. Use when captured requests contain live tokens, cookies, API keys or another person's personal data"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, redaction, privacy]
---

# Transcript Redaction

> Redact credentials and third-party personal data from transcripts without destroying the evidence the triager needs

**Use when:** captured requests contain live tokens, cookies, API keys or another person's personal data

**Avoid when:** the evidence is fully synthetic and contains no real credential or personal data

## Procedure

1. Search the transcript for authorization headers, cookies and API keys.
2. Replace each secret with a stable placeholder that keeps the field name and length class.
3. Replace third-party personal data with a marker that preserves the field, not the value.
4. Confirm the redacted transcript still shows the request shape and the response difference.
5. Re-run the PoC with a fake credential to prove the placeholder is not needed to reproduce.
6. Keep an unredacted copy outside the repository and never attach it.

## Signals

- A bearer token appears in a committed file or a screenshot.
- The response body contains another user's email or phone number.
- A cookie value in the transcript is still valid and reusable.
- Redaction removed the header that actually mattered to the finding.

## Patterns

**1. Stable placeholder**

```text
Authorization: Bearer {{alice_token}}
Cookie: session={{alice_session}}  -> reproducible, not usable
```

**2. Preserve the finding**

```text
response field email: {{victim_email}}  -> the disclosure is still visible
```

**3. Prove the placeholder is safe**

```text
replay with a fresh token  -> same effect, so the redaction cost nothing
```

## Pitfalls

- Committing a live token and only removing it in a later commit, which keeps it in history.
- Redacting so aggressively that the request no longer shows the vulnerable parameter.
- Replacing values with the same fake string everywhere, erasing the cross-identity difference.

## Done when

- No live credential or third-party personal data appears in shipped artifacts.
- The redacted transcript still demonstrates the effect.

## References

- [OWASP - sensitive data exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)
- [CWE-312 - cleartext storage of sensitive information](https://cwe.mitre.org/data/definitions/312.html)

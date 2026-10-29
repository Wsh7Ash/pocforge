---
name: asset-to-spec-mapping
description: "Map every claim in the draft PoC onto one concrete asset and one concrete request, so nothing in the writeup rests on a hostname the researcher never touched. Use when a draft PoC mixes several hosts, environments or API versions and it is unclear which one actually produced the effect"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [scope, frame, evidence]
---

# Asset to Spec Mapping

> Map every claim in the draft PoC onto one concrete asset and one concrete request, so nothing in the writeup rests on a hostname the researcher never touched

**Use when:** a draft PoC mixes several hosts, environments or API versions and it is unclear which one actually produced the effect

**Avoid when:** the PoC is a single request against a single host, where mapping adds bookkeeping without adding evidence

## Procedure

1. List every host, port and API version that appears anywhere in the draft writeup.
2. For each one, record whether you sent a request to it or merely saw it in a response body.
3. Delete claims about hosts you never sent a request to, or mark them explicitly as unverified context.
4. Confirm the surviving asset appears in the program scope under its own line.
5. Pin the spec's asset field to the exact host and path prefix you exercised.
6. Re-read the steps and check each one names the same asset the spec declares.

## Signals

- The writeup says production but the captured Host header shows staging.
- One step targets v1 and another targets v2 without saying so.
- An internal hostname appears only inside a JSON error message.
- The asset field is a bare domain while the steps use a deep path prefix.

## Patterns

**1. One asset per spec**

```text
asset: https://api.example.com/v2
steps all start with /v2/  -> consistent
step 4 uses /v1/orders  -> split into a second spec
```

**2. Separate touched from observed**

```text
touched: api.example.com
observed only in an error body: db-shard-07.internal  -> context, not evidence
```

**3. Pin the version in the request**

```text
GET /v2/orders/1042 HTTP/1.1  Host: api.example.com  -> the version is in the path, not inferred from the docs
```

## Pitfalls

- Claiming impact on a host you only inferred from a banner or an error string.
- Letting the writeup drift between environments so triage cannot reproduce either one.
- Using a bare domain in the asset field while steps hit a path the program excludes.

## Done when

- Every step in the spec names the same declared asset.
- Observed-but-not-touched hosts are labelled as context, not evidence.

## References

- [OWASP WSTG - reporting and evidence](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/)
- [CWE - weakness reporting guidance](https://cwe.mitre.org/data/definitions/1000.html)

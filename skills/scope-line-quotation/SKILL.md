---
name: scope-line-quotation
description: "Copy the exact program scope line that covers the asset into the PoC before writing a single step, so authorization is never inferred from a hostname. Use when starting any PoC on a target whose program scope lists assets as wildcards, URL prefixes or excluded paths"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [scope, frame, triage]
---

# Scope Line Quotation

> Copy the exact program scope line that covers the asset into the PoC before writing a single step, so authorization is never inferred from a hostname

**Use when:** starting any PoC on a target whose program scope lists assets as wildcards, URL prefixes or excluded paths

**Avoid when:** the program publishes a machine-readable scope file you can link instead, which is stronger than a paraphrase

## Procedure

1. Open the program page and copy the asset line verbatim, including any wildcard or path prefix.
2. Record the retrieval timestamp and the page URL, because scope changes between report and triage.
3. Check the exclusions list separately: a covered host often excludes one path or admin subdomain.
4. Resolve your target to a hostname and confirm it matches the asset pattern rather than a lookalike.
5. Paste the quoted line into the spec's scope_ref field and mark the target authorized only now.
6. Re-check scope immediately before submission, and note any drift in the disclosure timeline.

## Signals

- The asset pattern uses a wildcard that does not cover your exact subdomain depth.
- The exclusions list names the endpoint you are about to attack.
- The scope page was edited after you captured your first request.
- Your target resolves through a third-party CDN the program does not list.

## Patterns

**1. Quote with the pattern intact**

```text
asset: *.example.com (wildcard, one label deep)
target: api.internal.example.com  -> two labels, NOT covered
```

**2. Record drift, do not assume**

```text
scope captured 2026-10-29T09:12Z
scope re-read 2026-10-29T15:40Z  -> exclusions list grew by /v2/admin
```

**3. Exclusion beats coverage**

```text
in scope: api.example.com
out of scope: api.example.com/v2/admin/*
-> a finding under /v2/admin is out of scope even though the host is listed
```

## Pitfalls

- Treating a wildcard as covering every subdomain depth, which is how out-of-scope reports get closed.
- Quoting the program's marketing page instead of the scope table that triage actually reads.
- Assuming a host in scope means every port and every virtual host on it is in scope.

## Done when

- The spec contains a verbatim scope quote with a retrieval timestamp.
- Any exclusion that touches the target path is listed in the spec.
- The authorized flag is set only after the quoted line was re-read.

## References

- [HackerOne - program scope policy guidance](https://docs.hackerone.com/en/articles/8475114-scope)
- [Bugcrowd - scope and exclusions](https://docs.bugcrowd.com/researchers/reporting-managing-submissions/scope/)

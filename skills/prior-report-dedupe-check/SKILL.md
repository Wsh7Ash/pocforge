---
name: prior-report-dedupe-check
description: "Search the program's disclosed reports and public advisories for the same root cause before investing in a full PoC, because duplicates are closed regardless of quality. Use when the bug is in a widely tested component, a popular framework or an endpoint that has had public writeups"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [triage, frame, duplicate]
---

# Prior Report Dedupe Check

> Search the program's disclosed reports and public advisories for the same root cause before investing in a full PoC, because duplicates are closed regardless of quality

**Use when:** the bug is in a widely tested component, a popular framework or an endpoint that has had public writeups

**Avoid when:** the target is a private build with no public disclosure history you can search

## Procedure

1. Search disclosed reports on the program page for the endpoint path and the parameter name.
2. Search the product's changelog and security advisories for a fix that matches your behaviour.
3. Search the component's upstream repository issues for the same root cause.
4. Compare the root cause, not the symptom: a different endpoint with the same missing check is still a duplicate.
5. Record what you searched and what you found, so the report shows the check was done.
6. If a prior fix exists, test whether the fix is incomplete before writing anything up.

## Signals

- The changelog mentions a hardening release on the endpoint you are testing.
- An upstream issue describes the same missing check in a sibling function.
- The program has a public report with the same parameter name and a different path.
- Your trigger only works on a version older than the latest release notes.

## Patterns

**1. Search by root cause**

```text
symptom: id parameter accepted on /export
root cause: missing ownership check before serialisation  -> search the root cause too
```

**2. Check whether the fix is partial**

```text
advisory fixed /orders/{id}
your test hits /orders/{id}/items  -> possibly the same root cause, still unfixed
```

**3. Record the negative search**

```text
searched: /export, export_id, tenant_id
found: 2 disclosed reports, both on /export/csv  -> this path is new
```

## Pitfalls

- Searching only the exact URL and missing the same defect behind a sibling route.
- Assuming a public advisory means the deployed build is patched.
- Skipping the search and discovering the duplicate after writing a full report.

## Done when

- The spec records which searches were run and what they returned.
- Any prior fix is either ruled out or shown to be incomplete with a request.

## References

- [HackerOne - duplicate report handling](https://docs.hackerone.com/en/articles/8475114-scope)
- [CVE - search published advisories](https://www.cve.org/)

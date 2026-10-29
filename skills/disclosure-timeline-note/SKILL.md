---
name: disclosure-timeline-note
description: "Record when the issue was found, reported and disclosed so the history is verifiable and the embargo terms are explicit. Use when the finding may be published later, or the program has a disclosure policy with fixed windows"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, disclosure, process]
---

# Disclosure Timeline Note

> Record when the issue was found, reported and disclosed so the history is verifiable and the embargo terms are explicit

**Use when:** the finding may be published later, or the program has a disclosure policy with fixed windows

**Avoid when:** the program forbids public disclosure entirely and a timeline note would only add confusion

## Procedure

1. Record the discovery date, the report date and the date each build was tested.
2. Quote the program's disclosure window and any extension the vendor requested.
3. Note which artifacts can be published and which contain third-party data.
4. Ask for written confirmation before publishing, and keep the reply.
5. Publish only after the fix is verified or the window has elapsed.
6. Update the timeline if the vendor extends the embargo, with the reason recorded.

## Signals

- The program's policy window differs from the platform default.
- The report contains another tenant's data that cannot be published.
- The vendor asked for an extension without giving a date.
- A public writeup already exists for the same bug, changing the embargo rationale.

## Patterns

**1. Timeline block**

```text
found 2026-10-24, reported 2026-10-25, fixed 2026-11-02, disclosed 2026-12-01
```

**2. Quote the window**

```text
program policy: 90 days from report, extension by written request
```

**3. Publish-safe evidence**

```text
publish the raw request with redacted tokens; withhold the victim's personal data
```

## Pitfalls

- Publishing before the vendor confirms the fix, which can re-expose live customers.
- Recording approximate dates that contradict the platform's own timestamps.
- Assuming the platform default window overrides the program's stated policy.

## Done when

- Discovery, report and disclosure dates are recorded and consistent with the platform.
- The published artifact set excludes third-party personal data.

## References

- [HackerOne - disclosure policy](https://docs.hackerone.com/en/articles/8475114-scope)
- [CVE - CNA disclosure rules](https://www.cve.org/ResourcesSupport/AllResources/CNARules)

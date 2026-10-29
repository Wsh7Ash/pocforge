---
name: evidence-manifest-build
description: "Assemble the evidence directory and its manifest as one atomic step, so the file set the report cites is exactly the set that was hashed. Use when packaging a report that cites several captures, screenshots and logs"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, evidence, integrity]
---

# Evidence Manifest Build

> Assemble the evidence directory and its manifest as one atomic step, so the file set the report cites is exactly the set that was hashed

**Use when:** packaging a report that cites several captures, screenshots and logs

**Avoid when:** the platform accepts only a single screenshot and no attachments

## Procedure

1. Freeze the evidence directory: no new captures until the report is submitted.
2. Name every file after the claim it supports rather than after a timestamp.
3. Hash the frozen directory into a manifest and record the manifest digest.
4. Reference each file by its manifest path inside the report body.
5. Re-verify the manifest immediately before uploading.
6. Reopen the submitted report and check every attachment arrived.

## Signals

- A capture is missing from the upload but present in the manifest.
- A filename in the report does not exist in the directory.
- The platform renamed an attachment, breaking your reference.
- The manifest digest in the report differs from the uploaded manifest.

## Patterns

**1. Frozen set**

```text
evidence/*.http, evidence/*.png, evidence/manifest.json  -> no edits after hashing
```

**2. Name by claim**

```text
cross-tenant-read.http, control-denied.http, cleanup-204.http
```

**3. Reference by path**

```text
see evidence/cross-tenant-read.http (sha256 4c1f...)
```

## Pitfalls

- Adding a capture after hashing and shipping a manifest that no longer matches.
- Naming files by timestamp so the reader cannot map claims to artifacts.
- Trusting the upload UI without reopening the report to confirm attachments.

## Done when

- The manifest verifies against the uploaded set with zero drift.
- Every claim in the report resolves to a manifest path.

## References

- [RFC 6234 - secure hash algorithms](https://www.rfc-editor.org/rfc/rfc6234)
- [HackerOne - report attachments](https://docs.hackerone.com/en/articles/8475114-scope)

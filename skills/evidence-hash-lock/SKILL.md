---
name: evidence-hash-lock
description: "Hash every artifact into a manifest and re-verify it before submission, so nobody can claim the evidence was edited after the fact. Use when the finding is disputed, high value, or will be reviewed by a second party such as a vendor security team"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, evidence, integrity]
---

# Evidence Hash Lock

> Hash every artifact into a manifest and re-verify it before submission, so nobody can claim the evidence was edited after the fact

**Use when:** the finding is disputed, high value, or will be reviewed by a second party such as a vendor security team

**Avoid when:** the platform only accepts inline text and no artifact can be attached

## Procedure

1. Collect every artifact the report cites into one directory.
2. Hash each file with SHA-256 and record size and relative path in a manifest.
3. Write the manifest next to the evidence and attach both to the report.
4. Re-run verification before submitting and after any file moves.
5. Replace the manifest whenever an artifact is added or corrected.
6. Quote the manifest digest in the report so the set is pinned to one line.

## Signals

- A file size changed after you last opened it, which means it was rewritten.
- The manifest lists a file that is no longer in the directory.
- An artifact was re-captured by hand and no longer matches its hash.
- The report cites a screenshot that is not in the manifest at all.

## Patterns

**1. Build and verify**

```text
pocforge hash evidence/ --write evidence/manifest.json
pocforge verify evidence/manifest.json --root evidence
```

**2. Pin the set**

```text
manifest_sha256: 9f2c...  -> one line identifies the whole evidence set
```

**3. Unrecorded file is a finding**

```text
verify reports unrecorded files  -> they were added after the lock
```

## Pitfalls

- Editing an artifact after hashing and shipping the stale manifest.
- Hashing only the big captures and leaving small ones unprotected and unrecorded.
- Publishing the manifest without the files, which proves nothing to a reader.

## Done when

- The manifest verifies with zero drift against the shipped evidence set.
- The report cites the manifest digest.

## References

- [RFC 6234 - US secure hash algorithms](https://www.rfc-editor.org/rfc/rfc6234)
- [NIST - hash function guidance](https://csrc.nist.gov/projects/hash-functions)

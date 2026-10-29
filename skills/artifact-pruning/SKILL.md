---
name: artifact-pruning
description: "Trim the evidence set to files a triager will actually open, while keeping every artifact that proves a distinct claim. Use when the evidence folder has grown to dozens of screenshots and near-duplicate captures"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, evidence, triage]
---

# Artifact Pruning

> Trim the evidence set to files a triager will actually open, while keeping every artifact that proves a distinct claim

**Use when:** the evidence folder has grown to dozens of screenshots and near-duplicate captures

**Avoid when:** the program explicitly requires a full capture set for its own review process

## Procedure

1. List every artifact and the specific claim it supports.
2. Delete artifacts that support no claim, such as exploratory screenshots.
3. Merge near-duplicate captures into one file that shows the difference clearly.
4. Keep one artifact per claim and one failed attempt per bound you assert.
5. Rename files so their names describe the claim, not the timestamp.
6. Rebuild the evidence manifest after pruning so hashes match the shipped set.

## Signals

- Ten screenshots differ only by scroll position.
- A capture shows an intermediate state no step in the report mentions.
- Filenames are timestamps, so a reader cannot tell which file is load-bearing.
- The manifest lists files that are no longer referenced anywhere.

## Patterns

**1. Claim to file map**

```text
claim: cross-tenant read -> evidence/cross-tenant-read.http
claim: cleanup succeeded -> evidence/cleanup-204.http
```

**2. Merge duplicates**

```text
screenshot-1..9 -> one side-by-side image showing baseline and effect
```

**3. Rehash after pruning**

```text
pocforge hash evidence/ --write evidence/manifest.json  -> hashes match the shipped set
```

## Pitfalls

- Shipping a hundred files that make the one real capture impossible to find.
- Deleting the failed attempt that bounded the claim and then still asserting the bound.
- Pruning files after hashing and leaving a manifest that no longer verifies.

## Done when

- Every shipped artifact maps to a claim in the report.
- The evidence manifest verifies against the pruned set.

## References

- [HackerOne - attaching evidence](https://docs.hackerone.com/en/articles/8475114-scope)
- [OWASP - evidence collection](https://owasp.org/www-project-web-security-testing-guide/)

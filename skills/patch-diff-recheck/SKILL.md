---
name: patch-diff-recheck
description: "Re-run the PoC after a vendor patch and diff the behaviour, so the retest proves the fix rather than assuming a changelog entry. Use when the vendor says the issue is fixed, or a new build has shipped since the report"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, retest, patch]
---

# Patch Diff Recheck

> Re-run the PoC after a vendor patch and diff the behaviour, so the retest proves the fix rather than assuming a changelog entry

**Use when:** the vendor says the issue is fixed, or a new build has shipped since the report

**Avoid when:** no fix has been deployed yet and you are only confirming the bug still exists

## Procedure

1. Capture the pre-patch response as the reference for the same request.
2. Confirm the deployed build or version changed, and record how you confirmed it.
3. Replay the identical PoC steps against the patched build.
4. Diff the new response against the reference and list every difference.
5. Check the legitimate path as well, to ensure the fix did not only break the exploit.
6. Report one of three verdicts: fixed, partially fixed, or not fixed, with evidence.

## Signals

- The trigger now returns 403 while the legitimate path still returns 200.
- The response is identical to the reference, meaning the fix did not deploy.
- The trigger fails but a variant path still works, indicating a partial fix.
- The legitimate path now fails too, which is a regression worth reporting.

## Patterns

**1. Three verdicts**

```text
fixed: trigger denied, legit path works
partial: trigger denied, variant path still works
not fixed: trigger unchanged
```

**2. Confirm the build**

```text
GET /healthz -> {"version": "2.14.1"}  -> the version the fix shipped in
```

**3. Diff, do not eyeball**

```text
diff results/pre-patch.http results/post-patch.http  -> every change is evidence
```

## Pitfalls

- Assuming a changelog entry means the fix reached the asset you tested.
- Testing only the exploit path and missing that the fix broke normal use.
- Re-playing a modified PoC and attributing the change to the patch.

## Done when

- The deployed build is identified by an observed response, not by a release note.
- The retest states fixed, partial or not fixed with a response diff.

## References

- [CWE - patch and retest guidance](https://cwe.mitre.org/)
- [OWASP - vulnerability management](https://owasp.org/www-community/vulnerability_management)

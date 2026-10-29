---
name: regression-guard-script
description: "Ship the PoC as a script that fails when the bug is fixed, so the same artifact serves as proof today and as a regression test after the patch. Use when the program accepts retests, or the fix will need verification weeks after submission"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [verify, tooling, retest]
---

# Regression Guard Script

> Ship the PoC as a script that fails when the bug is fixed, so the same artifact serves as proof today and as a regression test after the patch

**Use when:** the program accepts retests, or the fix will need verification weeks after submission

**Avoid when:** the program forbids retaining automation against its assets after the report closes

## Procedure

1. Convert the PoC into a script with explicit configuration flags for host and credentials.
2. Make the script assert the vulnerable condition and exit zero only when it holds.
3. Add a documented mode that asserts the fixed condition for post-patch runs.
4. Store the script in the repository with a README line showing both invocations.
5. Run both modes against the current build and record the results.
6. Note in the report that the script doubles as a regression test for the fix.

## Signals

- The script exits zero even when the effect is absent, so it cannot detect a fix.
- Configuration is hard-coded to a host that will be decommissioned.
- The fixed mode passes before the patch, meaning the assertion is wrong.
- The script needs an interactive login that automation cannot perform.

## Patterns

**1. Two modes**

```text
repro.sh --expect vulnerable  -> exit 0 while the bug exists
repro.sh --expect fixed       -> exit 0 only after the patch
```

**2. Assert, do not print**

```text
assert status == 200 and victim_marker in body  -> the exit code is the oracle
```

**3. Document both runs**

```text
vulnerable mode: pass
fixed mode: fail (expected, no patch yet)
```

## Pitfalls

- Writing a script that prints the response but asserts nothing, so it never fails.
- Hard-coding credentials into the script and leaking them when the repo goes public.
- Shipping a fixed-mode assertion that already passes, which would hide a fix.

## Done when

- Both modes run against the current build with the expected exit codes.
- The report tells the vendor how to use the script as a regression test.

## References

- [Python - unittest assertions](https://docs.python.org/3/library/unittest.html)
- [OWASP - security regression testing](https://owasp.org/www-project-web-security-testing-guide/)

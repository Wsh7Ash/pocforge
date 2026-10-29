---
name: one-line-repro-distillation
description: "Compress the whole PoC into a single copy-pasteable command, which is the strongest signal that the bug is understood rather than witnessed. Use when the PoC is a numbered narrative and you want a form a triager can run in ten seconds"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, reproduce, tooling]
---

# One-Line Repro Distillation

> Compress the whole PoC into a single copy-pasteable command, which is the strongest signal that the bug is understood rather than witnessed

**Use when:** the PoC is a numbered narrative and you want a form a triager can run in ten seconds

**Avoid when:** the flow genuinely needs a browser, an interactive login or multiple identities that cannot be scripted

## Procedure

1. Reduce the PoC to a scripted sequence with extracted values and no manual steps.
2. Bundle the sequence behind one command with configuration passed as flags.
3. Make the command print the one line that shows the effect, plus the status code.
4. Test the command in a clean shell with only the documented environment variables set.
5. Paste the exact command into the reproduction field of the spec.
6. Keep the script in the repository so the command stays runnable after submission.

## Signals

- The command needs three undocumented exports to work.
- Output is a wall of JSON where one field carries the proof.
- The script depends on a file in your home directory.
- A triager would have to read the source to know whether it worked.

## Patterns

**1. Print the proof line**

```text
printf 'status=%s owner=%s\n' "$CODE" "$OWNER"  -> one line a triager can paste back
```

**2. Flags over editing**

```text
repro.sh --base https://api.example.com --alice "$A" --bob "$B"  -> no file edits
```

**3. Fail loudly**

```text
exit non-zero when the effect is absent  -> CI and triage agree on what success means
```

## Pitfalls

- Shipping a script that only works on your machine because of an unset default.
- Printing the whole response body and hiding the single field that proves the claim.
- Exiting zero when the effect did not appear, which makes the script useless as an oracle.

## Done when

- One documented command reproduces the effect from a clean shell.
- The command exits non-zero when the effect is absent.

## References

- [curl - manual page](https://curl.se/docs/manpage.html)
- [OWASP - proof of concept expectations](https://owasp.org/www-project-web-security-testing-guide/)

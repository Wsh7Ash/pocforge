# Security and scope

## What this tool is

`pocforge` grades written proofs of concept. It sends no requests, opens no sockets and reads only the files you point it at.

It is not an exploitation framework, and nothing in it attacks anything.

## Authorized testing only

Every skill here assumes a program that permits the testing, and the grader enforces that assumption: a spec without a `scope_ref` and an explicit `authorized: true` cannot reach grade A. That is a reporting rule, not a licence. It does not make a test legal, and passing the grader does not make a target in scope.

If you are unsure whether an asset is covered, stop and read the program's scope page. `pocforge show scope-line-quotation` exists because "the hostname looked like it was covered" is how researchers get banned.

## Stop conditions

The corpus expects a declared stop condition on any PoC that touches delete, refund, invite, payment or bulk export. The defaults that apply to this project's own examples:

- No request may target a record, address or account the PoC did not create.
- No notification may be sent to an address the researcher does not control.
- No brute force against identifiers belonging to another tenant.

## Credentials and personal data

- Specs and evidence are expected to contain placeholders such as `{{alice_token}}`, never live secrets.
- Evidence manifests hash artifacts; they do not make them safe to publish. Redact before you ship, then re-hash.
- The example evidence in this repository is synthetic: `example.test` addresses and invented tokens.

## Reporting a problem in this tool

Open an issue describing the input that produced the wrong grade. A grader that passes a spec it should reject is a security-relevant bug in this project, because someone will rely on the grade.

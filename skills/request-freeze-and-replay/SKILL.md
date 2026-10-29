---
name: request-freeze-and-replay
description: "Freeze the exact bytes of the working request into a file and replay from that file, so reproduction does not depend on a live proxy session or a browser. Use when the trigger was found by hand-editing traffic and needs to become a durable, shareable artifact"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, tooling, evidence]
---

# Request Freeze and Replay

> Freeze the exact bytes of the working request into a file and replay from that file, so reproduction does not depend on a live proxy session or a browser

**Use when:** the trigger was found by hand-editing traffic and needs to become a durable, shareable artifact

**Avoid when:** the trigger needs a browser-only flow such as a WebAuthn assertion that cannot be replayed from bytes

## Procedure

1. Dump the working request to a file as raw HTTP, preserving header order and duplicates.
2. Store credentials as placeholders rather than literals so the file can be shared safely.
3. Replay the file with a raw client that sends your bytes unchanged.
4. Confirm the replayed response matches the response you observed manually.
5. Record the exact command used to replay, with placeholders documented.
6. Commit the request file next to the PoC so a triager can run it in one step.

## Signals

- A client library reorders headers or drops duplicates, changing the result.
- The trigger works in the browser but not when rebuilt by a library call.
- The request contains a duplicated header that a normal client cannot produce.
- Replaying the saved file produces a different status than the manual test.

## Patterns

**1. Raw request file**

```text
POST /v2/orders HTTP/1.1
Host: api.example.com
Content-Length: 27
Content-Type: application/json

{"sku":"A1","qty":2}
```

**2. Credential placeholder**

```text
Authorization: Bearer {{alice_token}}  -> substituted by the replay command, never committed
```

**3. One-command replay**

```text
replay --file trigger.http --set alice_token="$ALICE"  -> the command goes in the report
```

## Pitfalls

- Rebuilding the request from a high-level client and losing a header the server actually keyed on.
- Committing a live bearer token into the request file and leaking it publicly.
- Replaying without content-length, which changes framing and can hide the effect.

## Done when

- A raw request file exists and reproduces the effect when replayed.
- The replay command is recorded with credentials as placeholders.

## References

- [RFC 9112 - HTTP/1.1 message syntax and routing](https://www.rfc-editor.org/rfc/rfc9112.html)
- [curl - manual page](https://curl.se/docs/manpage.html)

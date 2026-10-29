---
name: header-stripping-descent
description: "Strip the request down to the headers that actually matter, so the PoC stops looking like a captured browser session and starts looking like a test. Use when the working request was copied from a browser and carries forty headers nobody has examined"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [minimize, headers, http]
---

# Header Stripping Descent

> Strip the request down to the headers that actually matter, so the PoC stops looking like a captured browser session and starts looking like a test

**Use when:** the working request was copied from a browser and carries forty headers nobody has examined

**Avoid when:** the target uses client-certificate or header-based authentication where most headers are load-bearing by design

## Procedure

1. Group headers into transport, authentication, content, client-identity and cosmetic.
2. Keep authentication and content headers, since removing them breaks the request legitimately.
3. Strip cosmetic headers such as accept-language and referer in one batch and re-test.
4. If the effect survives, remove them permanently; if not, bisect the batch.
5. Test whether a browser user-agent is required by replacing it with a minimal one.
6. Publish the surviving header list in the exact order the server accepts.

## Signals

- The effect disappears when the browser user-agent is replaced.
- A client-identity header such as X-Requested-With is required.
- Content-Type must be exactly application/json with no charset suffix.
- Removing a header changes the response from JSON to an HTML error page.

## Patterns

**1. Tier the headers**

```text
auth: Authorization, Cookie
content: Content-Type, Content-Length
cosmetic: Accept-Language, Referer, Sec-Fetch-*
```

**2. Batch then bisect**

```text
strip 12 cosmetic headers -> effect survives -> delete all 12
```

**3. Minimal browser UA**

```text
User-Agent: ExampleApp/7.2.1  -> only if the server branches on it
```

## Pitfalls

- Stripping Content-Length, which changes framing and silently invalidates the test.
- Keeping Sec-Fetch and Accept-Language headers that only make the PoC look copied.
- Assuming a header is cosmetic when the server actually keys a cache or route on it.

## Done when

- Every surviving header has a recorded reason to be there.
- The effect still reproduces with the reduced header set.

## References

- [RFC 9110 - header fields](https://www.rfc-editor.org/rfc/rfc9110.html)
- [MDN - forbidden request headers](https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_request_header)

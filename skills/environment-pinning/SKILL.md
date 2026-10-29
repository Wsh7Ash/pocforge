---
name: environment-pinning
description: "Pin the client version, region, protocol and transport the PoC needs, because many defects only appear on one client build or through one edge. Use when the target serves multiple clients, regions or protocol versions and the effect appeared in only one of them"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [reproduce, environment, method]
---

# Environment Pinning

> Pin the client version, region, protocol and transport the PoC needs, because many defects only appear on one client build or through one edge

**Use when:** the target serves multiple clients, regions or protocol versions and the effect appeared in only one of them

**Avoid when:** the endpoint behaves identically across clients and the request has no version-dependent headers

## Procedure

1. Record the client identifier, version and platform headers the working request used.
2. Record the region or edge node if the response exposes one.
3. Send the same request with a different client version and note whether the effect survives.
4. Send it through a different network path or region where that is within scope.
5. Document the configuration that reproduces and any that do not.
6. Strip environment headers that turn out not to matter before finalising.

## Signals

- The mobile client gets different validation than the web client for the same endpoint.
- A region-specific edge returns the unpatched behaviour.
- The effect depends on TLS or HTTP version negotiation.
- A feature-gated client build is the only one that accepts the payload.

## Patterns

**1. Pin the client**

```text
User-Agent: ExampleApp/7.2.1 (android)
X-Client-Version: 721  -> both recorded, both required
```

**2. Test the other client**

```text
same path with web UA -> 400  -> note that the defect is client-specific
```

**3. Record negatives**

```text
reproduces: android 7.2.1, ios 7.2.1
does not: web 5.0  -> scope the claim to the mobile clients
```

## Pitfalls

- Omitting the client version header from the PoC and leaving triage unable to reproduce.
- Assuming a defect found on one client affects all of them without testing.
- Pinning a header that turned out to be irrelevant, which narrows the claim for no reason.

## Done when

- The spec lists the client and protocol configuration required to reproduce.
- At least one non-reproducing configuration is recorded as a bound.

## References

- [RFC 9110 - user agent and content negotiation](https://www.rfc-editor.org/rfc/rfc9110.html)
- [OWASP - mobile application security testing](https://owasp.org/www-project-mobile-app-security/)

---
name: screenshot-provenance
description: "Make each screenshot self-evidencing with the URL, identity and timestamp visible, so it cannot be dismissed as an unrelated or edited image. Use when the report relies on UI screenshots to show cross-account data or an admin-only view"
pack: pocforge
version: 1.0.0
category: bug-bounty-poc
tags: [package, evidence, screenshots]
---

# Screenshot Provenance

> Make each screenshot self-evidencing with the URL, identity and timestamp visible, so it cannot be dismissed as an unrelated or edited image

**Use when:** the report relies on UI screenshots to show cross-account data or an admin-only view

**Avoid when:** the same claim is already proven by a raw request and response pair

## Procedure

1. Capture the full browser window including the address bar and any account indicator.
2. Show the identity that produced the view, such as the avatar or account menu.
3. Pair each screenshot with the raw request that produced the page.
4. Add a short caption naming the claim and the step number it belongs to.
5. Crop only irrelevant chrome, never the address bar or identity indicator.
6. Store screenshots in the evidence manifest like any other artifact.

## Signals

- A cropped image shows data but no URL or account context.
- The screenshot is from a different host than the spec declares.
- The UI shows a shared view that would legitimately display the data.
- The image metadata shows an edit after capture.

## Patterns

**1. Context in frame**

```text
address bar: /orders/1042
account menu: bob@example.test
timestamp widget: 09:41 UTC
```

**2. Pair with bytes**

```text
screenshot shows the render; evidence/cross-tenant-read.http shows the source of truth
```

**3. Caption the claim**

```text
Figure 2: bob's session renders alice's order (step 3)
```

## Pitfalls

- Cropping out the address bar, which removes the only proof of which host was hit.
- Using a screenshot as the sole evidence for a claim that a response body proves better.
- Editing an image for legibility and destroying its provenance.

## Done when

- Each screenshot shows URL, identity and a caption tied to a step.
- Every screenshot claim also has a raw response in the evidence set.

## References

- [OWASP - evidence and screenshots](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - report attachments](https://docs.hackerone.com/en/articles/8475114-scope)

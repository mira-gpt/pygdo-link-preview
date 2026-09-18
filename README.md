# pygdo-link-preview

PyGDOv8 module for deterministic link-preview images.

It lets an administrator assign an explicit preview image to a method, for
example:

```text
$link_preview.set dog_website.home https://example.org/images/home-card.png
```

Pages without an explicit image can use a static screenshot fallback from:

```text
files/link_preview/<method-trigger-with-dots-replaced-by-underscores>.png
```

The screenshot is intentionally pre-rendered by an external scheduled job
(such as Playwright), never captured during a visitor request. This keeps the
OpenGraph path fast and prevents user-controlled URLs from being rendered by
the server.

## Integration

Website/meta renderers call:

```python
PreviewResolver.for_method(method.gdo_trigger())
```

If it returns a URL/path, emit it as `og:image`; otherwise retain the site
default. The module does not override an image explicitly supplied by a page.

## Status

The module provides persistent method-to-image management and a safe static
screenshot fallback resolver. Wiring the resolver into a particular website
renderer is intentionally one small integration point, since individual
PyGDO sites own their meta rendering.

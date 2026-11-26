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
the server. This applies to the existing method-preview fallback.

## Markdown preview images

For public Markdown file previews, `MarkdownPreview.for_html(rendered, style)`
creates a 1200 × 630 PNG on the first request and returns an absolute URL. It
caches images by the SHA-256 of the rendered HTML and style; subsequent
requests reuse the file and changed content gets a new URL. A single
non-blocking render lock limits concurrent browser starts; while another render
is running, the page is served without an image. Rendering has a timeout and
fails open to the ordinary Markdown preview if unavailable. Generated images
are stored in `gdo/link_preview/public/generated/` and are not committed.

The isolated Chromium process receives HTML rather than a URL, disables
JavaScript and service workers, and blocks resource requests. External images
and fonts therefore do not appear. The core Markdown preview integration
requests screenshots only for non-SEO, publicly served, non-symlink files.
Do not use this API with private or token-protected content: cached images are
public. A working sandboxed `/usr/bin/chromium` and Python Playwright package
are required. The first request can take several seconds; each unique
rendered page consumes disk until its cached file is removed by an operator.

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

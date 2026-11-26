"""Isolated screenshot helper; HTML comes from stdin, not from a URL."""

import sys

from playwright.sync_api import sync_playwright


def main():
    document = sys.stdin.buffer.read(256 * 1024 + 1)
    if len(document) > 256 * 1024 or len(sys.argv) != 2:
        raise SystemExit(2)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', chromium_sandbox=True)
        try:
            context = browser.new_context(viewport={'width': 1200, 'height': 630},
                                          java_script_enabled=False, service_workers='block')
            context.route('**/*', lambda route: route.abort())
            page = context.new_page()
            page.set_default_timeout(8000)
            page.set_content(document.decode('utf-8'), wait_until='domcontentloaded')
            page.screenshot(path=sys.argv[1], type='png', timeout=8000)
        finally:
            browser.close()


if __name__ == '__main__':
    main()

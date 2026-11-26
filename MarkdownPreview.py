"""Cached, network-isolated screenshots of public Markdown previews."""

import fcntl
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from gdo.base.Application import Application


class MarkdownPreview:
    MAX_INPUT = 256 * 1024

    @classmethod
    def for_html(cls, rendered: str, style: str) -> str | None:
        """Return an absolute image URL, or None if rendering is unavailable."""
        document = ('<!doctype html><html><head><meta charset="utf-8"><style>'
                    + style + '</style></head><body>' + rendered + '</body></html>')
        data = document.encode('utf-8')
        if len(data) > cls.MAX_INPUT:
            return None
        digest = hashlib.sha256(b'markdown-preview-v1\0' + data).hexdigest()
        cache_dir = Path(Application.file_path('gdo/link_preview/public/generated'))
        target = cache_dir / (digest + '.png')
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            if target.is_file():
                return cls._url(digest)
            with (cache_dir / '.render.lock').open('a') as lock:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    return None
                if not target.is_file():
                    fd, name = tempfile.mkstemp(prefix='.render-', suffix='.png', dir=cache_dir)
                    os.close(fd)
                    try:
                        python = str(Path(sys.prefix) / 'bin' / 'python3')
                        subprocess.run(
                            [python, '-m', 'gdo.link_preview.markdown_screenshot', name],
                            input=data, cwd=Application.file_path(),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            timeout=15, check=True,
                        )
                        os.chmod(name, 0o644)
                        os.replace(name, target)
                    finally:
                        if os.path.exists(name):
                            os.unlink(name)
        except (OSError, subprocess.SubprocessError):
            return None
        return cls._url(digest)

    @staticmethod
    def _url(digest: str) -> str:
        scheme = 'https' if Application.is_tls() or Application.config('core.force_tls', '0') == '1' else 'http'
        root = Application.web_root().rstrip('/')
        return f'{scheme}://{Application.domain()}{Application.get_current_port()}{root}/gdo/link_preview/public/generated/{digest}.png'

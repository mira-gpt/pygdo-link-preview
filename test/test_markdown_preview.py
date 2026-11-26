import tempfile
import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch

from gdo.base.Application import Application
from gdo.link_preview.MarkdownPreview import MarkdownPreview


class MarkdownPreviewTest(unittest.TestCase):
    def test_cache_reuses_image_and_invalidates_when_content_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def fake_run(command, **kwargs):
                Path(command[-1]).write_bytes(b'png')

            with patch.object(Application, 'file_path', side_effect=lambda path='': str(root / path)), \
                    patch.object(Application, 'is_tls', return_value=True), \
                    patch.object(Application, 'domain', return_value='example.test'), \
                    patch.object(Application, 'web_root', return_value='/'), \
                    patch.object(Application, 'get_current_port', return_value=''), \
                    patch('gdo.link_preview.MarkdownPreview.subprocess.run', side_effect=fake_run) as run:
                first = MarkdownPreview.for_html('<h1>A</h1>', 'body {}')
                self.assertEqual(first, MarkdownPreview.for_html('<h1>A</h1>', 'body {}'))
                second = MarkdownPreview.for_html('<h1>B</h1>', 'body {}')
            self.assertNotEqual(first, second)
            self.assertEqual(2, run.call_count)
            self.assertTrue(first.startswith('https://example.test/gdo/link_preview/public/generated/'))

    def test_oversized_content_is_not_rendered(self):
        with patch('gdo.link_preview.MarkdownPreview.subprocess.run') as run:
            self.assertIsNone(MarkdownPreview.for_html('x' * MarkdownPreview.MAX_INPUT, ''))
            run.assert_not_called()

    def test_renderer_failure_returns_no_image(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(Application, 'file_path', side_effect=lambda path='': str(Path(directory) / path)), \
                patch('gdo.link_preview.MarkdownPreview.subprocess.run', side_effect=subprocess.TimeoutExpired('renderer', 15)):
            self.assertIsNone(MarkdownPreview.for_html('<p>test</p>', ''))
            self.assertEqual([], list(Path(directory).rglob('*.png')))

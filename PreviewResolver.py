from pathlib import Path

from gdo.base.Application import Application
from gdo.link_preview.GDO_LinkPreview import GDO_LinkPreview


class PreviewResolver:
    """Resolve a managed image, otherwise a pre-rendered method screenshot.

    Screenshots are deliberately generated out of request scope. A scheduled
    renderer can save `<method-trigger>.png` below `files/link_preview/`; page
    rendering then only serves a stable static file.
    """

    @staticmethod
    def for_method(trigger: str) -> str | None:
        preview = GDO_LinkPreview.table().get_by_val('lp_method', trigger)
        if preview:
            return preview.gdo_val('lp_image')
        filename = trigger.replace('.', '_') + '.png'
        path = Path(Application.files_path(f'link_preview/{filename}'))
        return str(path) if path.is_file() else None

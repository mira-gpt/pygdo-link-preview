from gdo.base.GDO_Module import GDO_Module


class module_link_preview(GDO_Module):
    """Managed OpenGraph images with a deterministic screenshot fallback."""

    def gdo_dependencies(self) -> list[str]:
        return ['file', 'net']

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_String import GDT_String
from gdo.net.GDT_Url import GDT_Url


class GDO_LinkPreview(GDO):
    """An explicit preview image assigned to one PyGDO method trigger."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('lp_id'),
            GDT_String('lp_method').not_null().maxlen(128).unique(),
            GDT_Url('lp_image').not_null().maxlen(1024),
        ]

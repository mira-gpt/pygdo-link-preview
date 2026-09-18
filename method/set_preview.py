from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_String import GDT_String
from gdo.net.GDT_Url import GDT_Url
from gdo.link_preview.GDO_LinkPreview import GDO_LinkPreview


class set_preview(Method):
    """Create or replace the managed image for a method trigger."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'link_preview.set'

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_String('method').not_null().maxlen(128).positional(),
            GDT_Url('image').not_null().maxlen(1024).positional(),
        ]

    def gdo_execute(self) -> GDT:
        method = self.param_val('method')
        image = self.param_val('image')
        preview = GDO_LinkPreview.table().get_by_val('lp_method', method)
        if preview:
            preview.save_val('lp_image', image)
        else:
            GDO_LinkPreview.blank({'lp_method': method, 'lp_image': image}).insert()
        return self.reply('msg_link_preview_saved', (method,))

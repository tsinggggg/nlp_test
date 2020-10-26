from ...core import ToggleButton
from ...flavours.html import templates


class HTMLToggleButton(ToggleButton):
    def render(self):
        return templates.template("togglebutton.html").render(**self.content)
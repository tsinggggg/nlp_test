from ...core import ToggleRow
from ...flavours.html import templates


class HTMLToggleRow(ToggleRow):
    def render(self):
        return templates.template("togglerow.html").render(**self.content)

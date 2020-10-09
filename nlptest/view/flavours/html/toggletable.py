from ...core import ToggleTable
from ...flavours.html import templates


class HTMLToggleTable(ToggleTable):
    def render(self):
        return templates.template("toggletable.html").render(**self.content)

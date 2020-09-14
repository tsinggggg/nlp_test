from ...core import Table
from ...flavours.html import templates


class HTMLTable(Table):
    def render(self):
        return templates.template("table.html").render(**self.content)

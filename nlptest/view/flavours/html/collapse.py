from ...core import Collapse
from ...flavours.html import templates


class HTMLCollapse(Collapse):
    def render(self):
        return templates.template("collapse.html").render(**self.content)
from ...core import TA
from ...flavours.html import templates


class HTMLTA(TA):
    def render(self):
        return templates.template("ta_detail.html").render(**self.content)

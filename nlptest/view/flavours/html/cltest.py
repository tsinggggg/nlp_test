from ...core import CLTest
from ...flavours.html import templates


class HTMLCLTest(CLTest):
    def render(self):
        return templates.template("cltest.html").render(**self.content)

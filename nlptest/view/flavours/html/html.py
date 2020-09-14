from ...core.html import HTML


class HTMLHTML(HTML):
    def render(self):
        return self.content["html"]
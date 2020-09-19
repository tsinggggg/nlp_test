from ...core import SentencePair
from ...flavours.html import templates


class HTMLSentencePair(SentencePair):
    def render(self):
        return templates.template("sentence_pair.html").render(**self.content)

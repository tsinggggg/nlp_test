from typing import Any

from ..abstract.item_renderer import ItemRenderer


class SentencePair(ItemRenderer):
    def __init__(self, string, **kwargs):
        super().__init__(
            "sentence_pair", {"string": string},
            **kwargs
        )

    def __repr__(self):
        return "SentencePair"

    def render(self) -> Any:
        raise NotImplementedError()

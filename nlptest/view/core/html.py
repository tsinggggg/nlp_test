from ..abstract.item_renderer import ItemRenderer
from typing import Any


class HTML(ItemRenderer):
    def __init__(self, content, **kwargs):
        super().__init__("html", {"html": content}, **kwargs)

    def __repr__(self):
        return "HTML"

    def render(self) -> Any:
        raise NotImplementedError()
from typing import Any

from ..abstract.item_renderer import ItemRenderer
from ..abstract.renderable import Renderable
from .togglebutton import ToggleButton


class Collapse(ItemRenderer):
    def __init__(self, button: ToggleButton, item: Renderable, **kwargs):
        super().__init__("collapse", {"button": button, "item": item}, **kwargs)

    def __repr__(self):
        return "Collapse"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv):
        obj.__class__ = cls
        if "button" in obj.content:
            flv(obj.content["button"])
        if "item" in obj.content:
            flv(obj.content["item"])
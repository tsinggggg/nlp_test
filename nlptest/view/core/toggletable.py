from typing import Any

from ..abstract.item_renderer import ItemRenderer


class ToggleTable(ItemRenderer):
    def __init__(self, rows, name=None, caption=None, header=None, **kwargs):
        super().__init__(
            "toggletable", {"rows": rows, "name": name, "caption": caption, 'header': header},
            **kwargs
        )

    def __repr__(self):
        return "ToggleTable"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv) -> None:
        obj.__class__ = cls
        if "rows" in obj.content:
            for item in obj.content["rows"]:
                flv(item)

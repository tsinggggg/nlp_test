from typing import Any

from ..abstract.item_renderer import ItemRenderer


class ToggleRow(ItemRenderer):
    def __init__(self, row_index, content, toggle_content, **kwargs):
        super().__init__(
            "togglerow", {"row_index": row_index,
                          "content": content,
                          "toggle_content": toggle_content,
                          },
            **kwargs
        )

    def __repr__(self):
        return "ToggleRow"

    def render(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def convert_to_class(cls, obj, flv) -> None:
        obj.__class__ = cls
        if "toggle_content" in obj.content:
            for item in obj.content["toggle_content"]:
                flv(item)

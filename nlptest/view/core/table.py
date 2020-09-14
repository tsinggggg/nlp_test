from typing import Any

from ..abstract.item_renderer import ItemRenderer


class Table(ItemRenderer):
    def __init__(self, rows, name=None, caption=None, header=None, **kwargs):
        super().__init__(
            "table", {"rows": rows, "name": name, "caption": caption, 'header': header},
            **kwargs
        )

    def __repr__(self):
        return "Table"

    def render(self) -> Any:
        raise NotImplementedError()

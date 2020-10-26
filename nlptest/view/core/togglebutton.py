from typing import Any

from ..abstract.item_renderer import ItemRenderer


class ToggleButton(ItemRenderer):
    def __init__(self, text, target_id, **kwargs):
        super().__init__("toggle_button", {"text": text,
                                           "target_id": target_id,
                                           }, **kwargs)

    def __repr__(self):
        return "ToggleButton"

    def render(self) -> Any:
        raise NotImplementedError()
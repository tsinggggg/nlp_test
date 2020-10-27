from typing import Any

from ..abstract.item_renderer import ItemRenderer


class TA(ItemRenderer):
    def __init__(self,
                 examples,
                 **kwargs):
        super().__init__(
            "ta", {"examples": examples,
                       },
            **kwargs
        )

    def __repr__(self):
        return "TA"

    def render(self) -> Any:
        raise NotImplementedError()

    # @classmethod
    # def convert_to_class(cls, obj, flv) -> None:
    #     obj.__class__ = cls
    #     if "rows" in obj.content:
    #         for item in obj.content["rows"]:
    #             flv(item)

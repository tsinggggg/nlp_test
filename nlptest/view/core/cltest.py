from typing import Any

from ..abstract.item_renderer import ItemRenderer


class CLTest(ItemRenderer):
    def __init__(self,
                 test_name,
                 test_type,
                 capability,
                 description,
                 result,
                 name=None,
                 caption=None,
                 **kwargs):
        super().__init__(
            "cltest", {
                       "caption": caption,
                       "test_type": test_type,
                       "capability": capability,
                       "description": description,
                       "result": result,
                       },
            **kwargs
        )

    def __repr__(self):
        return "CLTest"

    def render(self) -> Any:
        raise NotImplementedError()

    # @classmethod
    # def convert_to_class(cls, obj, flv) -> None:
    #     obj.__class__ = cls
    #     if "rows" in obj.content:
    #         for item in obj.content["rows"]:
    #             flv(item)

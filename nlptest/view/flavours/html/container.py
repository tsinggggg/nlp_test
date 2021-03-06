from ...core import Container
from ..html import templates


class HTMLContainer(Container):
    def render(self):
        if self.sequence_type in ["list"]:
            return templates.template("sequence/list.html").render(
                anchor_id=self.content["anchor_id"], items=self.content["items"]
            )
        # elif self.sequence_type == "named_list":
        #     return templates.template("sequence/named_list.html").render(
        #         anchor_id=self.content["anchor_id"], items=self.content["items"]
        #     )
        elif self.sequence_type == "tabs":
            return templates.template("sequence/tabs.html").render(
                tabs=self.content["items"],
                anchor_id=self.content["anchor_id"],
                nested=self.content["nested"],
            )
        # elif self.sequence_type == "select":
        #     return templates.template("sequence/select.html").render(
        #         tabs=self.content["items"],
        #         anchor_id=self.content["anchor_id"],
        #         nested=self.content["nested"],
        #     )
        elif self.sequence_type == "sections":
            return templates.template("sequence/sections.html").render(
                sections=self.content["items"],
                # full_width=config["html"]["style"]["full_width"].get(bool),
            )
        elif self.sequence_type == "grid":
            return templates.template("sequence/grid.html").render(
                items=self.content["items"]
            )

        raise ValueError("Template not understood", self.sequence_type)
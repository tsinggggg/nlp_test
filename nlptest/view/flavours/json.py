import json
from ..core import *

class CustomEncoder(json.JSONEncoder):
    def key_to_json(self, o):
        if isinstance(o, Container):
            return o.name
        if isinstance(o, Table):
            return o.name
        if isinstance(o, TA):
            return o.name
        if isinstance(o, ToggleTable):
            return o.name
        if isinstance(o, ToggleRow):
            return o.row_index
        return None

    def default(self, o):
        if isinstance(o, Root):
            return self.default(o.content["body"])

        if isinstance(o, Container):
            return {self.key_to_json(x): self.default(x)
                    for x in o.content["items"]
                    if self.key_to_json(x) is not None}

        if isinstance(o, Table):
            if o.content["header"] is not None:
                return [
                        {h: v
                        for h, v in zip(o.content["header"],
                                        [r["name"]] + r["value"]
                                        )
                        }
                    for r in o.content["rows"]
                        ]

            else:
                return [
                        {r["name"]: r["value"][0]}
                        for r in o.content["rows"]
                       ]

        if isinstance(o, TA):
            return [
                {
                    'original_label': example["original_label"],
                    'perturbed_label': example["perturbed_label"],
                    'original_text': example["original_text"],
                    'perturbed_text': example["perturbed_text"]
                }
                for example in o.content["examples"]
            ]

        if isinstance(o, ToggleTable):
            return [
                self.default(row)
                for row in o.content['rows']
            ]

        return str(o)
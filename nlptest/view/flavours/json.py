import json
from ..core import *

class CustomEncoder(json.JSONEncoder):
    def key_to_json(self, o):
        if isinstance(o, Container):
            return o.name
        if isinstance(o, Table):
            return o.name
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

        return str(o)
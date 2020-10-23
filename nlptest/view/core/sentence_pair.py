from typing import Any

from ..abstract.item_renderer import ItemRenderer


class SentencePair(ItemRenderer):
    def __init__(self, original_label, perturbed_label, original_text, perturbed_text, **kwargs):
        super().__init__(
            "sentence_pair", {"original_label": original_label,
                              'perturbed_label': perturbed_label,
                              'original_text': original_text,
                              'perturbed_text': perturbed_text
                              },
            **kwargs
        )

    def __repr__(self):
        return "SentencePair"

    def render(self) -> Any:
        raise NotImplementedError()

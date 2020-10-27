from ..abstract.renderable import Renderable
from typing import Dict, Type


def apply_renderable_mapping(mapping, structure, flavour):
    for key, value in mapping.items():
        if isinstance(structure, key):
            value.convert_to_class(structure, flavour)


def get_html_renderable_mapping() -> Dict[Type[Renderable], Type[Renderable]]:
    """Workaround variable type annotations not being supported in Python 3.5
    Returns:
        type annotated mapping dict
    """
    from .html import (
        HTMLHTML,
        HTMLRoot,
        HTMLTable,
        HTMLContainer,
        HTMLSentencePair,
        HTMLToggleTable,
        HTMLToggleRow,
        HTMLCLTest,
        HTMLToggleButton,
        HTMLCollapse,
        HTMLTA,
    )
    from ..core import (
        HTML,
        Container,
        Root,
        Table,
        SentencePair,
        ToggleRow,
        ToggleTable,
        CLTest,
        ToggleButton,
        Collapse,
        TA,
    )
    return {
        HTML: HTMLHTML,
        Root: HTMLRoot,
        Container: HTMLContainer,
        Table: HTMLTable,
        SentencePair: HTMLSentencePair,
        ToggleRow: HTMLToggleRow,
        ToggleTable: HTMLToggleTable,
        CLTest: HTMLCLTest,
        ToggleButton: HTMLToggleButton,
        Collapse: HTMLCollapse,
        TA: HTMLTA,
    }


def HTMLReport(structure: Renderable):
    """Adds HTML flavour to Renderable
    Args:
        structure:
    Returns:
    """
    mapping = get_html_renderable_mapping()
    apply_renderable_mapping(mapping, structure, flavour=HTMLReport)
    return structure


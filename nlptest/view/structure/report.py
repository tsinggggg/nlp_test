from ..abstract.renderable import Renderable
from ..core import HTML, Root, Container, Table


def get_report_overview():
    test_info_cl = Table(
        [
            {
                "name": "Number of tests",
                "value": [2, 4, 6],
                "fmt": "fmt_number",
            },
        ],
        name="CL Test Summary",
        header=['capability', 'mft', 'inv', 'dir']
    )

    test_info_ta = Table(
        [
            {
                "name": "Attack Success rate",
                "value": [0.56],
                "fmt": "fmt_percent",
            },
        ],
        name="TA Test Summary"
    )

    return [Container(
        [test_info_cl],
        anchor_id="cl_overview",
        name="CL",
        sequence_type="grid",
    ),
        Container(
            [test_info_ta],
            anchor_id="ta_overview",
            name="TA",
            sequence_type="grid",
        )
    ]


def get_report_structure(
) -> Renderable:

    section_items = []

    section_items.append(
        Container(
            get_report_overview(),
            sequence_type="tabs",
            name="Overview",
            anchor_id="overview",
        )
    )
    sections = Container(section_items, name="Root", sequence_type="sections")
    footer = HTML(
        content='NLP tests utilizing <a href="https://github.com/marcotcr/checklist">checklist</a>.'
    )
    return Root("Root", sections, footer)

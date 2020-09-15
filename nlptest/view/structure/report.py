from ..abstract.renderable import Renderable
from ..core import HTML, Root, Container, Table


def get_report_overview(results):
    ret = []
    if "checklist" in results:
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
        ret.append(
            Container(
                [test_info_cl],
                anchor_id="cl_overview",
                name="CL",
                sequence_type="grid",
            ))

    from ...nlptest.testsuite.ta.ta_testsuite import get_result_from_logger
    if 'textattack' in results:
        ta_summary = get_result_from_logger(results['textattack'])
        test_info_ta = Table(
            [
                {
                    "name": k,
                    "value": [v],
                    "fmt": "fmt_numeric",
                }
                for k, v in ta_summary.items()
            ],
            name="TA Test Summary"
        )
        ret.append(
            Container(
                [test_info_ta],
                anchor_id="ta_overview",
                name="TA",
                sequence_type="grid",
            ))

    return ret


def get_report_structure(results
                         ) -> Renderable:
    section_items = []

    section_items.append(
        Container(
            get_report_overview(results),
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

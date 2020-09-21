from ..abstract.renderable import Renderable
from ..core import HTML, Root, Container, Table, SentencePair
from textattack.loggers import attack_log_manager


def get_report_overview(results):
    ret = []
    if "checklist" in results:
        from ...nlptest.testsuite.cl_test.cl_testsuite import get_summary_from_test_suite
        cl_summary = get_summary_from_test_suite(results["checklist"])
        cl_summary = cl_summary.pivot('capability', 'type', ['testcases', 'fails'])
        test_info_cl = Table(
            [
                {
                    "name": cap,
                    "value": [(row['fails', t] / row['testcases', t], row['testcases', t])
                              if ('testcases', t) in row.index else (0, 0)
                              for t in ['MFT', 'INV', 'DIR']],
                    "fmt": "fmt_pct_numeric_pair",
                }
                for cap, row in cl_summary.iterrows()
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


def get_ta_detail(logger: attack_log_manager):
    results = logger.results
    ret = [SentencePair(string=x.__str__('file')) for x in results]
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
    # each sentence/result of text attack
    if "textattack" in results:
        section_items.append(
            Container(
                get_ta_detail(results["textattack"]),
                sequence_type="list",
                name="TA result",
                anchor_id="ta_result",
            )
        )
    sections = Container(section_items, name="Root", sequence_type="sections")
    footer = HTML(
        content='NLP tests utilizing <a href="https://github.com/marcotcr/checklist">checklist</a>, <a href="https://github.com/QData/TextAttack">textattack</a>.'
    )
    return Root("Root", sections, footer)

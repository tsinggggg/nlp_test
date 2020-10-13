import collections
from ..abstract.renderable import Renderable
from ..core import HTML, Root, Container, Table, SentencePair, ToggleTable, ToggleRow
from textattack.loggers import AttackLogManager


def get_report_overview(results):
    ret = []
    if "checklist" in results:
        from ...nlptest.testsuite.cl_test.cl_testsuite import get_summary_from_test_suite
        cl_summary = get_summary_from_test_suite(results["checklist"])

        test_info_cl = Table(
            [
                {
                    "name": cap,
                    "value": [(tests[t]['fail_rate'], tests[t]['cases'])
                              for t in ['MFT', 'INV', 'DIR']],
                    "fmt": "fmt_pct_numeric_pair",
                }
                for cap, tests in cl_summary.items()
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


def get_ta_detail(logger: AttackLogManager):
    results = logger.results
    ret = [SentencePair(string=x.__str__('file')) for x in results]
    return ret


def get_cl_detail(testsuite):
    test_types = ['MFT', 'INV', 'DIR']
    from ...nlptest.testsuite.cl_test.cl_testsuite import get_summary_from_test_suite
    cl_summary = get_summary_from_test_suite(testsuite)
    _rows = []
    for cap in cl_summary.keys():

        _toggle_content = []
        for t in test_types:
            tests = [x for x in testsuite.tests if (testsuite.info[x]['type'] == t)
                     and (testsuite.info[x]['capability'] == cap)]
            if len(tests) == 0:
                continue

            table_content = []
            for test in tests:
                stats = testsuite.tests[test].get_stats()
                table_content.append({"name": test,
                                      "value": [(stats['fails'] / stats['testcases'], stats['testcases'])
                                                ],
                                      "fmt": "fmt_pct_numeric_pair", })
            _toggle_content.append(Table(
                table_content,
                name="CL-" + cap + "-" + t + " Test Summary",
                header=['test name', 'failure rate']
            ))
        toggle_content = Container(_toggle_content,
                                   anchor_id=cap + "_detail",
                                   name=cap,
                                   sequence_type="list",
                                   )
        this_row = ToggleRow(row_index=cap,
                             content=[
                                 {
                                     "name": cap,
                                     "value": [(cl_summary[cap][t]['fail_rate'],
                                                cl_summary[cap][t]['cases'])
                                               for t in test_types],
                                     "fmt": "fmt_pct_numeric_pair",
                                 }
                             ],
                             toggle_content=[toggle_content],
                             )

        _rows.append(this_row)
    ret = ToggleTable(header=['capability'] + test_types,
                      name="CL result table",
                      rows=_rows,
                      anchor_id="cl_result_table"
                     )
    # ret = [SentencePair(string=x.__str__('file')) for x in results]
    return [ret]


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
    if "checklist" in results:
        section_items.append(
            Container(
                get_cl_detail(results["checklist"]),
                sequence_type="list",
                name="CL result",
                anchor_id="cl_result",
            )
        )
    sections = Container(section_items, name="Root", sequence_type="sections")
    footer = HTML(
        content='NLP tests utilizing <a href="https://github.com/marcotcr/checklist">checklist</a>, <a href="https://github.com/QData/TextAttack">textattack</a>.'
    )
    return Root("Root", sections, footer)

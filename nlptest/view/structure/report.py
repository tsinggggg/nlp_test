import collections
from ..abstract.renderable import Renderable
from ..core import HTML, Root, Container, Table, SentencePair, ToggleTable, ToggleRow, CLTest, ToggleButton, TA
from textattack.loggers import AttackLogManager


def get_report_overview(results):
    test_description = """A Minimum Functionality test (<b>MFT</b>), inspired by unit tests in software engineering, 
    is a collection of simple examples (and labels) to check a behavior within a capability. <br>
    An Invariance test (<b>INV</b>) is when we apply label-preserving perturbations to inputs and expect the model 
    prediction to remain the same.<br>
    A Directional Expectation test (<b>DIR</b>) is similar to INV, except that the label is expected to change in 
    a certain way.<br>
    <a href='https://www.aclweb.org/anthology/2020.acl-main.442.pdf'>Link to reference</a>
    """

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
            header=['Capability', 'Minimum Functionality Test', 'INVariance Test', 'DIRectional Expectation Test']
        )
        desc = HTML(
            f'<div id="cl_explain" style="padding:20px" class="collapse"><div class="card card-body"><p>{test_description}</p></div></div>',
        )

        ret.append(
            Container(
                [test_info_cl,
                 ToggleButton(
                     "Toggle tests descriptions",
                     "cl_explain",
                     anchor_id="toggle-tests-description",
                     name="Toggle tests descriptions",
                 ),
                 desc
                 ],
                anchor_id="cl_overview",
                name="CL",
                sequence_type="list",
            )
            )

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
    from textattack.attack_results import SuccessfulAttackResult, SkippedAttackResult, FailedAttackResult
    def _get_original_result_str(r):
        output_label = r.original_result.raw_output.argmax()
        confidence_score = r.original_result.raw_output[output_label]
        output_str = f"{output_label} ({confidence_score:.0%})"
        return output_str
    def _get_successful_result_str(r):
        output_label = r.perturbed_result.raw_output.argmax()
        confidence_score = r.perturbed_result.raw_output[output_label]
        output_str = f"{output_label} ({confidence_score:.0%})"
        return output_str
    def _get_skipped_result_str(r):
        return "SKIPPED"
    def _get_failed_result_str(r):
        return "FAILED"
    results = logger.results
    # ret = [SentencePair(string=x.__str__('file')) for x in results]
    ret = []
    for r in results:
        output_str = _get_original_result_str(r)
        original_text = r.original_text()
        perturbed_text = None
        if isinstance(r, SkippedAttackResult):
            perturbed_output_str = _get_skipped_result_str(r)
        elif isinstance(r, SuccessfulAttackResult):
            perturbed_output_str = _get_successful_result_str(r)
            perturbed_text = r.perturbed_text()
        elif isinstance(r, FailedAttackResult):
            perturbed_output_str = _get_failed_result_str(r)
        ret.append(dict(original_label=output_str,
                                perturbed_label=perturbed_output_str,
                                original_text=original_text,
                                perturbed_text=perturbed_text
                                ))
    return [TA(examples=ret)]


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
                # table_content.append({"name": test,
                #                       "value": [(stats['fails'] / stats['testcases'], stats['testcases'])
                #                                 ],
                #                       "fmt": "fmt_pct_numeric_pair", })
                table_content.append(
                ToggleRow(row_index=test,
                          content=[
                              {
                                  "name": test,
                                  "value": [(stats['fails'] / stats['testcases'], stats['testcases'])
                                            ],
                                  "fmt": "fmt_pct_numeric_pair",
                              }
                          ],
                          toggle_content=[CLTest(test_name=test,
                                                 test_type=t,
                                                 capability=cap,
                                                 description=testsuite.info[test]['description'],
                                                 result={'fail':stats['fails'],
                                                         'testcases': stats['testcases'],
                                                         'rate': stats['fails'] / stats['testcases'],
                                                         },
                                                 examples=testsuite.tests[test].form_testcases()
                                                 )],
                          )
                )
            # _toggle_content.append(Table(
            #     table_content,
            #     name= cap + "-" + t,
            #     header=['test name', 'failure rate']
            # ))
            _toggle_content.append(ToggleTable(
                header=['test name', 'failure rate'],
                name=cap + "-" + t,
                anchor_id=cap + "-" + t,
                rows=table_content,
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

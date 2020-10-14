import functools
import collections
import pandas as pd
from checklist.test_types import MFT, INV, DIR
from checklist.test_suite import TestSuite
from checklist.editor import Editor
from transformers import TextClassificationPipeline
from .predict_functions import predict_function_for_huggingface_pipeline
from ...config import config, _parse_perturb


def _create_MFT(data, labels, name=None, capability=None, description=None):
    """

    :param data: list of inputs(strings or ...)
    :param labels: single value or list of labels with the same length as data
    :param name:
    :param capability:
    :param description:
    :return:
    """
    test = MFT(data=data, labels=labels,
               name=name, capability=capability, description=description)
    return test


def _create_INV(data, name=None, capability=None, description=None):
    """

    :param data: list of inputs(strings or ...)
    :param name:
    :param capability:
    :param description:
    :return:
    """
    test = INV(data=data,
               name=name, capability=capability, description=description)
    return test


def create_MFT(dataset=None, templates=None, perturb=None, name=None, capability=None, description=None, **kwargs):
    """

    :param dataset: list of lists of input, label
    :param templates:
    :param name:
    :param capability:
    :param description:
    :return:
    """
    if templates is None and perturb is None:

        test = _create_MFT(data=[x[0] for x in dataset],
                           labels=[x[1] for x in dataset],
                           name=name, capability=capability, description=description
                           )
    elif perturb:
        from checklist.perturb import Perturb
        func = _perturb_functions(perturb['change'])
        features, targets = [x[0] for x in dataset], [x[1] for x in dataset]
        perturbed_data = Perturb.perturb(features,
                                         functools.partial(func,
                                                           phrases=perturb['phrases'])
                                         )
        # _flattened_data = [item for sublist in perturbed_data['data'] for item in sublist]
        # num_perturb = [len(x) for x in perturbed_data['data']]
        # _labels = []
        # for n, y in zip(num_perturb, targets):
        #     _labels.extend([y] * n)
        test = _create_MFT(data=perturbed_data['data'],
                           labels=targets,
                           name=name, capability=capability, description=description
                           )

    # elif templates:
    #     editor, ret = Editor(), None
    #     for t in templates:
    #         if ret is None:
    #             ret = editor.template(**t)
    #         else:
    #             ret += editor.template(**t)
    #     test = _create_MFT(**ret,
    #                        name=name, capability=capability, description=description
    #                        )
    else:
        raise ValueError('please provide at least one of dataset or templates for MFT')

    return test


def create_INV(dataset=None, templates=None, perturb=None, name=None, capability=None, description=None, **kwargs):
    """

    :param dataset: list of lists of input, label
    :param templates:
    :param name:
    :param capability:
    :param description:
    :return:
    """
    if perturb is not None:
        from checklist.perturb import Perturb
        func = _perturb_functions(perturb['change'])

        features, targets = [x[0] for x in dataset], [x[1] for x in dataset]
        perturbed_data = Perturb.perturb(features,
                                         functools.partial(func,
                                                           phrases=perturb['phrases'])
                                         )
        test = _create_INV(data=perturbed_data['data'],
                           name=name, capability=capability, description=description
                           )
    # elif templates:
    #     editor, ret = Editor(), None
    #     for t in templates:
    #         if ret is None:
    #             ret = editor.template(**t)
    #         else:
    #             ret += editor.template(**t)
    #     test = _create_MFT(**ret,
    #                        name=name, capability=capability, description=description
    #                        )
    else:
        raise ValueError('please provide at least one of dataset or templates for MFT')

    return test


def create_cl_testsuite(dataset):
    """

    :param dataset:
    :return:
    """
    suite = TestSuite()
    test_count = 0
    for test_name, test_config in config['checklist']['tests'].items():
        if test_config['type'].get(str) == "MFT":
            mft = create_MFT(dataset=dataset[:test_config['num_sentences'].get(int)],
                             name=test_name,
                             capability=test_config['capability'].get(str),
                             description=test_config['description'].get(str),
                             perturb=_parse_perturb(test_config['perturb'])
                             )
            suite.add(mft)
        elif test_config['type'].get(str) == "INV":
            inv = create_INV(dataset=dataset[:test_config['num_sentences'].get(int)],
                             name=test_name,
                             capability=test_config['capability'].get(str),
                             description=test_config['description'].get(str),
                             perturb=_parse_perturb(test_config['perturb'])
                             )
            suite.add(inv)
        else:
            continue
        test_count += 1

    if test_count == 0:
        raise ValueError("No tests provided")
    else:
        return suite


def run_cl_test(testsuite, pipeline):
    if isinstance(pipeline, TextClassificationPipeline):
        pred_f = functools.partial(predict_function_for_huggingface_pipeline,
                                   pipeline=pipeline)
    testsuite.run(pred_f)
    return testsuite


def get_summary_from_test_suite(testsuite):
    ret = pd.DataFrame()
    vals = collections.defaultdict(lambda: 100, {'MFT': 0, 'INV': 1, 'DIR': 2})
    capability_order = ['Vocabulary', 'Taxonomy', 'Robustness', 'NER', 'Fairness', 'Temporal', 'Negation', 'Coref',
                        'SRL', 'Logic']
    cap_order = lambda x: capability_order.index(x) if x in capability_order else 100
    caps = sorted(set([x['capability'] for x in testsuite.info.values()]), key=cap_order)
    for capability in caps:
        tests = [x for x in testsuite.tests if testsuite.info[x]['capability'] == capability]
        for n in tests:
            stats = testsuite.tests[n].get_stats()
            stats.update({'capability': capability}),
            stats.update({'test_name': n})
            stats.update({'type': testsuite.info[n]['type']})
            ret = ret.append(stats, ignore_index=True)
    ret = ret.pivot('capability', 'type', ['testcases', 'fails'])
    ret_dict = collections.OrderedDict()
    for cap, row in ret.iterrows():
        ret_dict[cap] = collections.OrderedDict()
        for t in ['MFT', 'INV', 'DIR']:
            if ('testcases', t) in row.index and \
                    (not pd.isna(row[('testcases', t)])):
                ret_dict[cap][t] = {'fail_rate': row['fails', t] / row['testcases', t],
                                    'cases': row['testcases', t],
                                    'fail': row['fails', t]
                                    }
            else:
                ret_dict[cap][t] = {'fail_rate': 0,
                                    'cases': 0,
                                    'fail': 0
                                    }
    return ret_dict


def _perturb_functions(change_to_make):
    if change_to_make == "append_to_end":
        def append_to_end(x, phrases):
            return ["%s %s"%(x, p) for p in phrases]
        return append_to_end
    elif change_to_make == "append_to_start":
        def append_to_start(x, phrases):
            return ["%s %s"%(x, p) for p in phrases]
        return append_to_start
    else:
        raise ValueError("not supported perturb")
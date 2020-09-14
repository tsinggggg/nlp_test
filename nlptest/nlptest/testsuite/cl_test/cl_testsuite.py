import functools
from checklist.test_types import MFT, INV, DIR
from checklist.test_suite import TestSuite
from checklist.editor import Editor
from transformers import TextClassificationPipeline
from .predict_functions import predict_function_for_huggingface_pipeline
from ...config import config


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


def create_MFT(dataset=None, templates=None, name=None, capability=None, description=None):
    """

    :param dataset: list of lists of input, label
    :param templates:
    :param name:
    :param capability:
    :param description:
    :return:
    """
    if dataset:

        # def get_iterator_for_data_at_index(data, ind):
        #     for i in data:
        #         # assuming this way of indexing works...
        #         # checklist does not accept genertor, will call len method
        #         yield i[ind]

        test = _create_MFT(data=[x[0] for x in dataset],
                           labels=[x[1] for x in dataset],
                           name=name, capability=capability, description=description
                           )
    elif templates:
        editor, ret = Editor(), None
        for t in templates:
            if ret is None:
                ret = editor.template(**t)
            else:
                ret += editor.template(**t)
        test = _create_MFT(**ret,
                           name=name, capability=capability, description=description
                           )
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
    if config['checklist']['MFT']['run'].get(bool):
        # customized mft
        if config['checklist']['MFT']['customized_mfts']:
            for t in config['checklist']['MFT']['customized_mfts']:
                mft = create_MFT(**t)
                suite.add(mft)
                test_count += 1
        # default mft
        mft = create_MFT(dataset=dataset[:config['checklist']['MFT']['num_sentences'].get(int)],
                         templates=None,
                         name='In Sample MFT',
                         capability='Correctness',
                         description='testing samples in train/test data'
                         )
        suite.add(mft)
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

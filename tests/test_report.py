from unittest import TestCase
import pandas as pd


def test_data():
    return   [['this is a good movie', 1],
               ['this is a bad movie', 0],
               ['this is a slightly positive review', 1],
               ['sdf asdf asdf asdf asdf asdfz vzxcvastr wer', 0],
               ['i am mad', 1],
               ['i am glad', 1],
               ['i had a great meal', 1],
               ['i am so sad', 0],
               ['i have no idea if i am happy', 0]
              ]


def test_case1():
    dataset = test_data()
    from transformers import pipeline
    p = pipeline("sentiment-analysis")
    model = p.model
    tokenizer = p.tokenizer
    return dataset, model, tokenizer


def test_case2():
    dataset = test_data()
    model = pd.read_pickle("./tf_idf_logistic_reg.pkl")
    tokenizer = pd.read_pickle("./tf_idf_vectorizor2.pkl")
    return dataset, model, tokenizer

class TestsTest(TestCase):

    def test_report(self):
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case1()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer)
        result = report.test_result
        result['checklist'].summary()
        result['textattack'].log_summary()
        with open('./out/report_1.html', 'w') as fh:
            fh.write(report.html)

    def test_report2(self):
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case2()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer)
        result = report.test_result
        result['checklist'].summary()
        result['textattack'].log_summary()
        with open('./out/report_2.html', 'w') as fh:
            fh.write(report.html)

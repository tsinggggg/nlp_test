from unittest import TestCase


def test_case1():
    dataset = [['this is a good movie', 1],
               ['this is a bad movie', 0],
               ['this is a slightly positive review', 1],
               ['today is monday', 1]
              ]
    from transformers import pipeline
    p = pipeline("sentiment-analysis")
    model = p.model
    tokenizer = p.tokenizer
    return dataset, model, tokenizer


class TestsTest(TestCase):

    def test_checklist_1(self):
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case1()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer)
        result = report.test_result
        result['checklist'].summary()
        result['textattack'].log_summary()
        pass

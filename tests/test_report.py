from unittest import TestCase
import json
import pathlib


current_path = pathlib.Path(__file__).parent.absolute()


def test_data():
    return [['this is a good movie', 1],
            ['this is a bad movie', 0],
            ['this is a slightly positive review', 1],
            ['i am mad', 0],
            ['i am glad', 1],
            ['i had a great meal', 1],
            ['i am so sad', 0],
            ['i have no idea if i am happy', 0]
            ]


def test_case_distillbert_binary():
    dataset = test_data()
    from transformers import pipeline
    p = pipeline("sentiment-analysis")
    model = p.model
    tokenizer = p.tokenizer
    return dataset, model, tokenizer


def test_case_bert_binary():
    dataset = test_data()
    from transformers import BertTokenizer, BertForSequenceClassification
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
    return dataset, model, tokenizer


def test_case_sklearn_binary():
    import pandas as pd
    dataset = test_data()
    model = pd.read_pickle("./tf_idf_logistic_reg.pkl")
    tokenizer = pd.read_pickle("./tf_idf_vectorizor2.pkl")
    return dataset, model, tokenizer


class TestsTest(TestCase):

    def test_report(self):
        """
        distill bert
        default embedding
        :return:
        """
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case_distillbert_binary()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer,
                           config_file=current_path / "config_test.yaml")
        result = report.test_result
        report_json = report.dict
        assert "Overview" in report_json.keys()
        assert "Adversarial Attacks" in report_json.keys()
        assert "Robustness Tests" in report_json.keys()
        assert "Robustness Tests" in report_json['Overview'].keys()
        assert "Adversarial Attacks" in report_json['Overview'].keys()
        assert "Tests Failure Rate" in report_json['Overview']['Robustness Tests'].keys()
        assert "Textattack Summary" in report_json['Overview']['Adversarial Attacks'].keys()
        with open(current_path / 'out/report_1.html', 'w') as fh:
            fh.write(report.html)

    def test_report_1_1(self):
        """
        distill bert
        default embedding but remove cos_sim_mat, mse_sim_mat
        :return:
        """
        from collections import defaultdict
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case_distillbert_binary()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer,
                           config_file=current_path / "config_test.yaml")
        test_suite = report.test_suite
        test_suite['textattack'].constraints[0].cos_sim_mat = defaultdict(dict)
        test_suite['textattack'].constraints[0].mse_sim_mat = defaultdict(dict)
        result = report.test_result
        with open(current_path / 'out/report_1_1.html', 'w') as fh:
            fh.write(report.html)

    def test_report2(self):
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case_sklearn_binary()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer)
        result = report.test_result
        with open(current_path / 'out/report_2.html', 'w') as fh:
            fh.write(report.html)

    def test_report3(self):
        """
        distill bert
        customized embedding
        :return:
        """
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case_distillbert_binary() # https://github.com/QData/TextAttack/issues/325
        dataset =  [['this is a good movie', 1]]
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer,
                           config_file=current_path / "config_test.yaml",
                           textattack={'customized_embedding': current_path / 'data/GoogleNews-vectors-negative300.bin'})
        result = report.test_result
        with open(current_path / 'out/report_3.html', 'w') as fh:
            fh.write(report.html)

    def test_report4(self):
        """
        bert
        :return:
        """
        from nlptest.nlptest.nlp_report import NLPReport
        dataset, model, tokenizer = test_case_bert_binary()
        report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer,
                           config_file=current_path / "config_test.yaml",
                           )
        result = report.test_result
        with open(current_path / 'out/report_4.html', 'w') as fh:
            fh.write(report.html)

from typing import Union
from pathlib import Path
import prompt_toolkit # this is a hack to solve the name conflict caused by wandb.vendor.prompt_toolkit
import os
import json
from .config import config
from ..utils.model_wrapper import model_wrapper


class NLPReport:
    """
    Generate a report of tests results
    dataset: an iterable of (text, ground_truth_output)
    """
    def __init__(self,
                 dataset,
                 model,
                 tokenizer,
                 config_file: Union[Path, str] = None,
                 **kwargs
                 ):
        if config_file is not None:
            config.set_file(config_file)

        config.set_kwargs(kwargs)

        os.environ['TA_CACHE_DIR'] = os.path.expanduser(config['rai_cache_path'].get(str))

        self.data = dataset
        self.model = model
        self.tokenizer = tokenizer
        self.pipeline = model_wrapper(model=model, tokenizer=tokenizer)

        self._report = None
        self._html = None
        self._widgets = None
        self._json = None
        self._dict = None
        self._test_suites = None
        self._test_results = None

    @property
    def test_suite(self):
        if self._test_suites is None:
            self._test_suites = dict()
            if config['checklist']['run'].get(bool):
                from .testsuite.cl_test.cl_testsuite import create_cl_testsuite
                self._test_suites['checklist'] = create_cl_testsuite(self.data)
            if config['textattack']['run'].get(bool):
                from .testsuite.ta.ta_testsuite import create_ta_recipe
                self._test_suites['textattack'] = create_ta_recipe(self.model,
                                                                   self.tokenizer,
                                                                   config['textattack']['recipe'].get(str)
                                                                   )
                if config['textattack']['customized_embedding'].get():
                    from .testsuite.ta.util import replace_word_embedding_for_recipe, gensim_wordvectors_for_ta
                    word_embedding = gensim_wordvectors_for_ta(config['textattack']['customized_embedding'].get(str))
                    self._test_suites['textattack'] = replace_word_embedding_for_recipe(self._test_suites['textattack'],
                                                                                        word_embedding
                                                                                        )
        return self._test_suites

    @property
    def test_result(self):
        if self._test_results is None:
            self._test_results = dict()
            if config['checklist']['run'].get(bool):
                from .testsuite.cl_test.cl_testsuite import run_cl_test
                testsuite = self.test_suite['checklist']
                self._test_results['checklist'] = run_cl_test(testsuite=testsuite,
                                                              pipeline=self.pipeline)
            if config['textattack']['run'].get(bool):
                from .testsuite.ta.ta_testsuite import run_ta_test
                attack = self.test_suite['textattack']
                self._test_results['textattack'] = run_ta_test(attack, self.data)

        return self._test_results

    @property
    def report(self):
        if self._report is None:
            from ..view.structure.report import get_report_structure
            self._report = get_report_structure(self.test_result)
        return self._report

    @property
    def html(self):
        if self._html is None:
            self._html = self._render_html()
        return self._html

    @property
    def json(self):
        if self._json is None:
            self._json = self._render_json()
        return self._json

    @property
    def dict(self):
        if self._dict is None:
            self._dict = json.loads(self.json)
        return self._dict
    #
    # @property
    # def widgets(self):
    #     if self._widgets is None:
    #         self._widgets = self._render_widgets()
    #     return self._widgets
    #
    def _render_html(self):
        from ..view.flavours.flavours import HTMLReport
        report = self.report
        html = HTMLReport(report).render(title="this_is_title")
        # with tqdm(total=1, desc="Render HTML", disable=disable_progress_bar) as pbar:
        #     html = HTMLReport(report).render(
        #        configs
        #     )
        #
        #     pbar.update()
        return html

    # def _render_widgets(self):
    #     pass
    #     # report = self.report
    #     # with tqdm(
    #     #         total=1, desc="Render widgets", disable=disable_progress_bar, leave=False
    #     # ) as pbar:
    #     #     widgets = WidgetReport(report).render()
    #     #     pbar.update()
    #     # return widgets
    #
    def _render_json(self):
        from ..view.flavours.json import CustomEncoder

        report = self.report
        data = json.dumps(report, indent=4, cls=CustomEncoder)
        return data
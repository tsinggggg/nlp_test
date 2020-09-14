from typing import Union
from pathlib import Path
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

        self.data = dataset
        self.model = model
        self.tokenizer = tokenizer
        self.pipeline = model_wrapper(model=model, tokenizer=tokenizer)

        self._report = None
        self._html = None
        self._widgets = None
        self._json = None
        self._test_suites = None
        self._test_results = None

    @property
    def test_suite(self):
        if self._test_suites is None:
            self._test_suites = dict()
            if config['checklist']['run'].get(bool):
                from .testsuite.cl_test.cl_testsuite import create_cl_testsuite
                self._test_suites['checklist'] = create_cl_testsuite(self.data)
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
        return self._test_results

    @property
    def report(self):
        if self._report is None:
            from ..view.structure.report import get_report_structure
            self._report = get_report_structure()
        return self._report

    @property
    def html(self):
        if self._html is None:
            self._html = self._render_html()
        return self._html

    # @property
    # def json(self):
    #     if self._json is None:
    #         self._json = self._render_json()
    #     return self._json
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
    # def _render_json(self):
    #     pass
    #     # with tqdm(total=1, desc="Render JSON", disable=disable_progress_bar) as pbar:
    #     #     data = json.dumps(description, indent=4, cls=CustomEncoder)
    #     #     pbar.update()
    #     # return data
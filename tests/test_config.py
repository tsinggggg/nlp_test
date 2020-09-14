from unittest import TestCase


class PathTest(TestCase):

    def test_config_load_default(self):
        from nlptest.nlptest.config import config
        assert config['title'].get(str) == "NLP Model Test Report"

    def test_config_set_attribute(self):
        from nlptest.nlptest.config import config
        new_title = "new_title"
        config.set_kwargs(dict(title=new_title))
        assert config['title'].get() == new_title

    def test_config_load_specify(self):
        from nlptest.nlptest.config import config
        from nlptest.utils.paths import get_config
        config.set_file(get_config("config_default.yaml"))
        assert config['title'].get(str) == "NLP Model Test Report"

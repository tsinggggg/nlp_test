from unittest import TestCase


class PathTest(TestCase):

    def test_config_path(self):
        from nlptest.utils.paths import get_config_default
        print(get_config_default())

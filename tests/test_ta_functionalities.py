from unittest import TestCase


class TestsTA(TestCase):

    def test_grammar_tool(self):
        class Text:
            def __init__(self, sentence):
                self.text = sentence

        # original_sentence = Text("this is a good movie")
        # perturbed_sentence = Text("this is a buon movie")
        original_sentence = Text("this is not an error")
        perturbed_sentence = Text("this is a error")
        from textattack.constraints.grammaticality.language_tool import LanguageTool
        language_tool = LanguageTool()
        assert (language_tool._check_constraint(perturbed_sentence,
                                                original_sentence) == False)
        assert (language_tool._check_constraint(original_sentence,
                                                perturbed_sentence) == True)

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

    def test_remove_cos_sim_mat(self):
        import os
        from collections import defaultdict
        os.environ['TA_CACHE_DIR'] = os.path.expanduser("~/.cache/rai")
        from textattack.constraints.semantics import WordEmbeddingDistance
        c = WordEmbeddingDistance(min_cos_sim=0.5)
        c.cos_sim_mat = defaultdict(dict) # should overwrite with default dict not dict
        c.get_cos_sim(1, 10)
        print(c.cos_sim_mat)


    def test_transform_embedding(self):
        from nlptest.nlptest.testsuite.ta.util import gensim_wordvectors_for_ta
        emb = gensim_wordvectors_for_ta('./data/GoogleNews-vectors-negative300.bin')
        pass

    # def test_numpy_cos_sim(self):
    #     import numpy as np
    #     vocab = 4
    #     top = 2
    #     cos_dist = np.array([[1, 0.1, 0.3, 0.2],
    #                          [0.1, 1, 0.5, 0.3 ],
    #                          [0.3, 0.5, 1, 0.9],
    #                          [0.2, 0.3, 0.9 ,1]])
    #     assert((cos_dist == cos_dist.T).all())
    #     np.sort(cos_dist, axis=1)[:, :(vocab - top - 1):-1]

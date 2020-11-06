from collections import defaultdict
import torch
import numpy as np


def gensim_wordvectors_for_ta(path):
    import gensim
    try:
        w2v_model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    except:
        raise Exception("not supported word embedding format")

    w2v_model.init_sims()
    VOCAB = len(w2v_model.index2word)
    top = 100
    # embedding matrix : Vocab * dim
    _embedding_mat = w2v_model.vectors_norm

    # this is unrealistic for huge vocab
    # cos_sim_mat = np.matmul(_embedding_mat, _embedding_mat.T)

    # word to ind dict
    _word2ind_dict = {w: ind for ind, w in enumerate(w2v_model.index2word)}
    # ind to word dict
    _ind2word_dict = {ind: w for ind, w in enumerate(w2v_model.index2word)}
    # cosine similarity
    # index: {index: similarity}
    # _cos_sim_dict = defaultdict(dict)
    # for x in range(len(w2v_model.index2word)):
    #     _temp_nn = w2v_model.most_similar(positive=[w2v_model.index2word[x]], topn=100)
    #     _temp_nn_dict = {_word2ind_dict[i[0]] : i[1] for i in _temp_nn}
    #     _ret = {x: 1}
    #     _ret.update(_temp_nn_dict)
    #     _cos_sim_dict[x] = _ret
    # _cos_sim_dict.update((ind,
    #                       dict([(ind, 1)] + w2v_model.most_similar(positive=[w2v_model.index2word[ind]],
    #                                                                topn=100)
    #                            )
    #                       )
    #                      for ind, w in enumerate(w2v_model.index2word)
    #                      )
    # mse similarity
    # index: {index: similarity}
    # _mse_dist_dict = defaultdict(dict)
    # _emb_tensor = torch.from_numpy(_embedding_mat)
    # _dist = torch.square(torch.cdist(_emb_tensor, _emb_tensor, p=2))
    # _rank = torch.argsort(_dist, dim=1)
    # _rank = _rank.numpy()
    # for i in range(len(w2v_model.index2word)):
    #     top_101_ind = _rank[i, :101]
    #     _temp_dist = _dist[i, :]
    #     _mse_dist_dict[i] = {top_w: _temp_dist[top_w].item() for top_w in top_101_ind}

    # nearest neighbours vocab * 101
    # _nn_mat = np.zeros((len(w2v_model.index2word), top + 1)).astype(int)
    class keyed_defaultdict(defaultdict):
        def __init__(self, f_of_key):
            super().__init__(None)
            self.f_of_key = f_of_key
        def __missing__(self, key):
            ret = self.f_of_key(key)
            self[key] = ret
            return ret
    def _lazy_nn(key, w2v=w2v_model, topn=top):
        return [key] + [w2v.index2word.index(i[0]) for i in w2v.similar_by_word(w2v.index2word[key],
                                                                                topn)
                        ]
    _nn_mat = keyed_defaultdict(_lazy_nn)
    # for k in _cos_sim_dict.keys():
    #     _nn_mat[k, :] = list(_cos_sim_dict[k].keys())

    return {"embedding_matrix": _embedding_mat,
            "w2i": _word2ind_dict,
            "i2w": _ind2word_dict,
            "cos_sim": defaultdict(dict),
            "mse_sim": defaultdict(dict),
            "nearest_neighbor": _nn_mat}


def replace_word_embedding_for_recipe(recipe, word_embedding):
    from textattack.constraints.semantics import WordEmbeddingDistance
    for c in recipe.constraints:
        if isinstance(c, WordEmbeddingDistance):
            c.word_embeddings = word_embedding['embedding_matrix']
            c.word_embedding_word2index = word_embedding['w2i']
            c.cos_sim_mat = word_embedding['cos_sim']
            c.mse_dist_mat = word_embedding['mse_sim']
    from textattack.transformations import WordSwapEmbedding
    t = recipe.transformation
    if isinstance(t, WordSwapEmbedding):
        t.nn = word_embedding['nearest_neighbor']
        t.word_embeddings = word_embedding['embedding_matrix']
        t.word_embedding_word2index = word_embedding['w2i']
        t.word_embedding_index2word = word_embedding['i2w']
    return recipe



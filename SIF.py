# -*- coding:utf8 -*-
# author:yaolinxia
# datetime:2020/3/11
# software: PyCharm
from gensim.models import KeyedVectors, word2vec

import pickle as pkl
import numpy as np
import jieba

word2vec_path = "data/models/word2vec_wiki.model" # 维基百科词向量
freq_table = 'data/output/wiki_voc.pkl' # 词频词典
embedding_size = 100
model = word2vec.Word2Vec.load(word2vec_path)


#定义分词函数
def cut(text): return ' '.join(jieba.cut(text))

global word_frequency
with open(freq_table, 'rb') as f:
    word_frequency = pkl.load(f)
print('完成词频字典载入')

# 简单SIF
def SIF_sentence_embedding(sen, alpha=1e-4):
    max_fre = max(word_frequency.values())
    sen_vec = np.zeros_like(model.wv['测试'])
    words = cut(sen).split()
    words = [w for w in words if w in model]
    for w in words:
        fre = word_frequency.get(w, max_fre)
        weight = alpha / (fre + alpha)
        sen_vec += weight * model.wv[w]

    sen_vec /= len(words)
    # skip SVD
    # print(sen_vec)
    return sen_vec


if __name__ == '__main__':
    text = "鹅额额额！"
    SIF_sentence_embedding(text)
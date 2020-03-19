import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import re
import nltk
from gensim.models import word2vec
from sklearn.manifold import TSNE
import random
# 汉字显示问题解决
import matplotlib.pyplot as plt
import matplotlib
matplotlib.matplotlib_fname()
import matplotlib.font_manager
"""
中文显示问题，试了以下四种方法，最终第四种方法奏效
"""
#### 1 macOS系统原因，字体换成Songti SC解决
matplotlib.rcParams['font.family'] = 'Songti SC'
matplotlib.rcParams['font.size'] = 10
#### 2
# plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
# plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#### 3
# myfont = matplotlib.font_manager.FontProperties(
#     fname='/Users/stone/Library/Fonts/SimHei.ttf')
# matplotlib.rcParams['axes.unicode_minus'] = False

#### 4
# plt.rcParams['font.family'] = ['sans-serif']
# plt.rcParams['font.sans-serif'] = ['SimHei']

# axes.unicode minus/Users/stone/PycharmProjects/Automatic-Corpus-Generation/ocr/msyh.ttc
# /Users/stone/PycharmProjects/Automatic-Corpus-Generation/ocr/msyh.ttc
def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    words = list(model.wv.vocab)
    random.shuffle(words)
    words = words[:500]
    for word in words:
        tokens.append(model[word])
        labels.append(word)
    # for word in model.wv.vocab:
    #     tokens.append(model[word])
    #     labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()

def test_view(model):
    # 因为词向量文件比较大，全部可视化就什么都看不见了，所以随机抽取一些词可视化
    words = list(model.wv.vocab)

    random.shuffle(words)
    words = words[:500]
    print("words", words)
    vector = model[words]
    tsne = TSNE(n_components=2, init='pca', verbose=1)
    embedd = tsne.fit_transform(vector)

    # 可视化
    plt.figure(figsize=(14, 10))
    plt.scatter(embedd[:300, 0], embedd[:300, 1])

    for i in range(300):
        x = embedd[i][0]
        y = embedd[i][1]
        plt.text(x, y, words[i])
    plt.show()

if __name__ == '__main__':
    vector_model = "word2vec_news2.model"
    wiki_vec = "data/models/word2vec_wiki.model"
    vec_model = word2vec.Word2Vec.load(wiki_vec)
    tsne_plot(vec_model)
    # test_view(vec_model)
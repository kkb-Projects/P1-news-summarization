from gensim.models import word2vec
from gensim.models.word2vec import PathLineSentences

import pandas as pd
pd.options.mode.chained_assignment = None
import random
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 词向量可视化
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

# 1. 训练词向量
def trainVector(inputpath="news_articles_cut.txt", outpath="word2vec_news2.model" ):
    model = word2vec.Word2Vec(PathLineSentences(inputpath),
                              size=100, window=5, min_count=2, workers=10)
    # tsne_plot(model)
    model.save(outpath)

# 2. 加载词向量
def testVector(vector_model="word2vec_news2.model"):
    vec_model = word2vec.Word2Vec.load(vector_model)
    res = vec_model.most_similar("勇敢")
    print("勇敢\n", res)
    res = vec_model.most_similar("美女")
    print("美女\n", res)
    print(vec_model["勇敢"])

# 3. 测试词向量
def analogy(x1, x2, y1, vector_model="word2vec_news2.model"):
    vec_model = word2vec.Word2Vec.load(vector_model)
    result = vec_model.most_similar(positive=[y1, x2], negative=[x1])
    return result[0][0]

def test_gensim():
    sents = [
    'I am a good student'.split(),
    'Good good study day day up'.split()
    ]
    print(sents)
    sents2 = "I am a good student Good good study day day up"
    # model = word2vec.Word2Vec(sents2, size=100, window=5, min_count=2, workers=10)
    model = word2vec.Word2Vec(PathLineSentences("news_articles_cut.txt"), size=100, window=5, min_count=5, workers=10)
    # 打印单词'good'的词向量
    print(model.wv.word_vec('此前'))
    # 打印和'good'相似的前2个单词
    print(model.wv.most_similar('此前', topn=2))
    # 保存模型到文件
    model.save('w2v.model')


if __name__ == '__main__':
    # 训练一个词向量
    # trainVector(outpath="data/models/word2vec_news_m2.model")
    # 训练wiki数据
    # trainVector(inputpath="data/output/wiki_cut.txt",
    #             outpath="data/models/word2vec_wiki.model" )
    wiki_vec = "data/models/word2vec_wiki.model"
    testVector(vector_model=wiki_vec)
    # vec_model = word2vec.Word2Vec.load(wiki_vec)
    # tsne_plot(vec_model)
    # test_vector(vec_model)
    # print(analogy('中国', '汉语', '美国'))
    # print(analogy('美国', '奥巴马', '美国'))
# -*- coding:utf8 -*-
# author:yaolinxia
# datetime:2020/3/11
# software: PyCharm

import random
import re
import pandas as pd
from collections import Counter
import jieba
from functools import reduce
"""
汉语新闻语料库处理
"""
def token(string):
    # we will learn the regular expression next course.
    return re.findall('\w+', string)

# 处理后的文本保存一下
def to_txt(articles_clean,outpath='news_articles.txt'):
    with open(outpath, 'w') as f:
        for a in articles_clean:
            f.write(a + '\n')

# 分词
def cut(string):
    return list(jieba.cut(string))

# 将token保存到dict在存储起来
def to_dict(Token, out_path='news_articles_dict.txt'):
    line_dict = {}
    with open(out_path, 'w') as f:
        for i, line in enumerate(Token):
            line_dict[i] = line
        f.write(str(line_dict))
    print(line_dict[2])

def seg2txt(Token, out_path='news_articles_cut.txt'):
    with open(out_path, 'w') as f:
        for line in Token:
            f.write(line+' ')

# 计算词频
def seg2num(cut_txt):
    c = Counter()
    with open(cut_txt, 'r') as f:
        for i in range(2):
            for lines in f.readlines():
                for l in lines.strip():
                    c[l] += 1
    for (k, v) in c.most_common(2):  # 输出词频最高的前两个词
        print("%s:%d" % (k, v))

if __name__ == '__main__':
    filename = 'data/sqlResult_1558435.csv'
    wiki_file = "data/wiki_00"
    wiki_out = "data/output/wiki_less.txt"
    """
        outpath = 'news_articles.txt'
        content = pd.read_csv(filename, encoding='gb18030')
        articles = content['content'].tolist()
        articles_clean = [''.join(token(str(a))) for a in articles]
        Token = []
        Token = cut(open(outpath).read())
        print("Token", Token)
        # to_dict(Token)
        seg2txt(Token)
    """
    seg2num("data/output/wiki_cut.txt")




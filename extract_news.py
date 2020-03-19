# -*- coding:utf8 -*-
# author:yaolinxia
# datetime:2020/3/11
# software: PyCharm

import pandas as pd
import re
from tqdm import tqdm
import SIF
"""
新闻中标题，全文，全文分词处理，并且获得相应句向量，存储到txt中
"""
def extract_sif(sif_txt="data/output/sif_embedding.txt", filename='data/sqlResult_1558435.csv'):
    content = pd.read_csv(filename, encoding='gb18030')
    contents = content['content'].tolist()
    titles = content['title'].tolist()
    with open(sif_txt, 'a' ) as f:
        for con,tit in tqdm(zip(contents, titles)):
            f.write("<sos>")
            f.write(str(tit)+' '+str(SIF.SIF_sentence_embedding(tit))+'\n')
            f.write(str(con)+' '+str(SIF.SIF_sentence_embedding(con))+'\n')
            for sen in sen_seg(con):
                f.write(str(sen)+' '+str(SIF.SIF_sentence_embedding(sen))+'\n')

# 短文划分成句子
def sen_seg(txt):
    pattern = r'\.|\?|!|。|；|！'
    result_list = re.split(pattern, str(txt).strip())
    return result_list

if __name__ == '__main__':
    extract_sif()

# -*- coding:utf-8 -*-
# author:asus
# datetime:2020/3/10 12:26
# software: PyCharm

from SIF import SIF_sentence_embedding
import re
import numpy as np


def split_Text(txt):
    pattern = r'\.|\?|!|。|！|\？'
    result_list = re.split(pattern, txt)
    return result_list


# def embedding(txt, title):
#     result_list = split_Text(txt)
#     txt_embedding = SIF_sentence_embedding(txt)
#     title_embedding = SIF_sentence_embedding(title)
#     embedding_list = []
#     for sen in result_list:
#         if sen != "":
#             embedding = SIF_sentence_embedding(sen)
#             embedding_list.append(embedding)
#     return txt_embedding, title_embedding, embedding_list


def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim


def abstract(txt, title):
    result_list = split_Text(txt)
    txt_embedding = SIF_sentence_embedding(txt)
    title_embedding = SIF_sentence_embedding(title)

    embedding_list = []
    for sen in result_list:
        if sen != "":
            embedding = SIF_sentence_embedding(sen)
            embedding_list.append(embedding)

    sim_weight_list = []
    for sen_embedding in embedding_list:
        sim_txt = cos_sim(sen_embedding, txt_embedding)
        sim_title = cos_sim(sen_embedding, title_embedding)
        sim_weight = 0.378 * sim_txt + 0.622 * sim_title
        sim_weight_list.append(sim_weight)
    # print(sim_weight_list)
    index_list = np.argsort(sim_weight_list)
    # print(index_list)

    # Cj加权求和
    i = 0
    while i < len(sim_weight_list):
        if i == 0:
            sim_weight_list[i] = 0.4 * sim_weight_list[i] + 0.3 * sim_weight_list[i + 1] + 0.3 * sim_weight_list[i + 2]
        if i == 1:
            sim_weight_list[i] = 0.2 * sim_weight_list[i - 1] + 0.4 * sim_weight_list[i] + 0.2 * sim_weight_list[i + 1] \
                                 + 0.2 * sim_weight_list[i + 2]
        if 1 < i < len(sim_weight_list) - 2:
            sim_weight_list[i] = 0.15 * sim_weight_list[i - 2] + 0.15 * sim_weight_list[i - 1] + 0.4 * sim_weight_list[
                i] \
                                 + 0.15 * sim_weight_list[i + 1] + 0.15 * sim_weight_list[i + 2]
        if i == len(sim_weight_list) - 2:
            sim_weight_list[i] = 0.2 * sim_weight_list[i - 2] + 0.2 * sim_weight_list[i - 1] + 0.4 * sim_weight_list[i] \
                                 + 0.2 * sim_weight_list[i + 1]
        if i == len(sim_weight_list) - 1:
            sim_weight_list[i] = 0.3 * sim_weight_list[i - 2] + 0.3 * sim_weight_list[i - 1] + 0.4 * sim_weight_list[i]
        i += 1
    # print(sim_weight_list)

    # 排序
    index_list = np.argsort(sim_weight_list)
    # print(index_list)
    # 前三句子生成摘要（按句子在文本顺序输出）
    a = index_list[-1]
    b = index_list[-2]
    c = index_list[-3]
    new_index_list = sorted([a, c, b])
    text_abstract = result_list[new_index_list[0]] + "。" + result_list[new_index_list[1]] + "。" \
                    + result_list[new_index_list[2]] + "。"
    # print(text_abstract)
    return text_abstract


if __name__ == '__main__':
    title = "突发！林肯公园主唱Chester自缢身亡 年仅41岁"
    txt = "网易娱乐7月21日报道  林肯公园主唱查斯特·贝宁顿Chester Bennington于今天早上，在洛杉矶 帕洛斯弗迪斯的一个私人庄园自缢身亡，" \
          "年仅41岁。此消息已得到洛杉矶警方证实。" \
          "洛杉矶警方透露，Chester的家人正在外地度假，Chester独自在家，上吊地点是家里的二楼。一说是一名音乐公司工作人员来家里找他时" \
          "发现了尸体，也有人称是佣人最早发现其死亡。" \
          "林肯公园另一位主唱麦克·信田确认了Chester Bennington自杀属实，并对此感到震惊和心痛，称稍后官方会发布声明。Chester昨天还在" \
          "推特上转发了一条关于曼哈顿垃圾山的新闻。粉丝们纷纷在该推文下留言，不相信Chester已经走了。" \
          "外媒猜测，Chester选择在7月20日自杀的原因跟他极其要好的朋友、Soundgarden（声音花园）乐队以及Audioslave乐队主唱" \
          "Chris Cornell有关，因为7月20日是Chris Cornell的诞辰。而Chris Cornell 于今年5月17日上吊自杀，享年52岁。" \
          "Chris去世后，Chester还为他写下悼文。" \
          "对于Chester的自杀，亲友表示震惊但不意外，因为Chester曾经透露过想自杀的念头，他曾表示自己童年时被虐待，导致他医生无法走出阴影，" \
          "也导致他长期酗酒和嗑药来疗伤。目前，洛杉矶警方仍在调查Chester的死因。" \
          "据悉，Chester与毒品和酒精斗争多年，年幼时期曾被成年男子性侵，导致常有轻生念头。Chester生前有过2段婚姻，育有6个孩子。" \
          "林肯公园在今年五月发行了新专辑《多一丝曙光One More Light》，成为他们第五张登顶Billboard排行榜的专辑。而昨晚刚刚发布" \
          "新单《Talking To Myself》MV。"
    text_abstract = abstract(txt, title)
    print(text_abstract)

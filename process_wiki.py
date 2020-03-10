import re
import jieba
import os
from tqdm import tqdm
from collections import Counter
import pickle

"""
维基百科数据处理
"""
# 去除空格等符号
def test_re(filepath="data/wiki_00"):
    sen = "<doc id=数学是>dsfjslf"
    s1 = re.findall(r'.*<(.*)>', "<doc id=数学是> \n<sdjksdjh>")
    cleaner = re.compile('<.*?>')
    print(cleaner)
    sen = re.sub(cleaner, ' ', sen)
    print(sen)
    print(s1)

# 对字符串进行分词
def cut(string):
    return list(jieba.cut(string))

# 去除空格等符号
def process_file(filepath="data/wiki_00", out_path="data/output/test.txt"):
    with open(filepath, 'r', encoding='utf-8') as f:
        with open(out_path, 'w', encoding='utf-8') as g:
            for line in tqdm(f.readlines()):
                if line.startswith("<") or line == '\n':
                    continue
                else:
                    for c in cut(line):
                        g.write(c+' ')

# 将维基百科语料分词保存
def process_dir(dir_path="/Users/stone/PycharmProjects/kkb_projects/wikiextractor/wiki_articles.txt",
                out_path="data/output/test.txt"):
    total_num = 0
    num_path = []
    files = os.listdir(dir_path)
    print("len_files", len(files))
    c = Counter()
    for f_ in files:
        if f_ != '.DS_Store':
            num_path.append(len(os.listdir(os.path.join(dir_path, f_))))
            for f2 in tqdm(os.listdir(os.path.join(dir_path, f_))):
                with open(os.path.join(os.path.join(dir_path, f_), f2), 'r', encoding='utf-8') as f:
                    with open(out_path, 'a', encoding='utf-8') as g:
                        for line in f.readlines():
                            # 去除一些特殊字符
                            line.strip('\n')
                            line = re.sub("[A-Za-z0-9\：\·\—\，\。\、\(\)\“\”\.\=\?\;\（\）\「\ 」\《\》]", "", line)
                            if line.startswith("<") or line == '\n':
                                continue
                            else:
                                total_num += 1
                                for c1 in cut(line):
                                    if len(c1) > 1 and c1 != '\r\n':
                                        c[c1] += 1
                                    g.write(c1+' ')
    print('\n词频统计结果：')
    for (k, v) in c.items():  # 输出词频最高的前两个词
        print("%s:%d" % (k, v))

    """
    total_nums 5615002
    len+files [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 27, 100, 100, 100]
    """
    print("total_nums", total_num)
    print("len+files", num_path)
    return c

# 存储到pkl文件
def pkl_out(dict_data, pkl_out):
    with open(pkl_out, 'wb') as fo:     # 将数据写入pkl文件
        pickle.dump(dict_data, fo)

# 分词+词频统计测试
def cut2():
    cut_words = ""
    for line in open('./text1.txt', encoding='utf-8'):
        line.strip('\n')
        line = re.sub("[A-Za-z0-9\：\·\—\，\。\“ \”]", "", line)
        seg_list = jieba.cut(line, cut_all=False)
        cut_words += (" ".join(seg_list))
    all_words = cut_words.split()
    print(all_words)
    c = Counter()
    for x in all_words:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    print('\n词频统计结果：')
    for (k, v) in c.most_common(2):  # 输出词频最高的前两个词
        print("%s:%d" % (k, v))

if __name__ == '__main__':
    """
    #test
    test_cut = "data/output/test_cut.txt"
    process_dir(dir_path="data/input", out_path=test_cut)
    """
    wiki_cut = "data/output/wiki_cut_filter.txt"
    pkl_file = "data/output/wiki_voc.pkl"
    wiki_data =process_dir(out_path=wiki_cut)
    pkl_out(wiki_data, pkl_file)
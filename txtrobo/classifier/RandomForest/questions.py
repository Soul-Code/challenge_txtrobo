from sklearn.feature_extraction.text import TfidfVectorizer as ti
import numpy as np
import jieba

PUNCTUATIONS = list('！!？?｡.＂"\'{}[]\\`~＃＄％＆＇（）()＊＋，-－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.')
STOPWORDS = ['请问', '的', '吗', '是', '我', '呢', '啊']
s2l = {'校车': '1', '校园网': '2', '银行、ATM': '3', '快递': '4', '打印店': '5', '在校事务': '6', '校医院': '7'}
jieba.load_userdict('../manualword.txt')


def load():
    dataset = []
    f = open('../manualdata.txt')
    for line in f.readlines():
        dataset.append(line.strip().split('\t'))
    dataset = np.array(dataset)
    # print(dataset)
    # model = ti()
    # print(ti.fit_transform(model, dataset[:, 0].tolist()).todense())
    # print(model.vocabulary_)

    # 获取词典
    vocabulary = []
    for i in range(dataset.shape[0]):
        vocabulary.extend(jieba.lcut(dataset[i][0]))
    vocabulary = set(vocabulary)
    # 移除标点符号
    for punc in PUNCTUATIONS:
        if punc in vocabulary:
            vocabulary.remove(punc)
    # 移除停用词
    for word in STOPWORDS:
        if word in vocabulary:
            vocabulary.remove(word)
    vocabulary = list(vocabulary)
    # print(vocabulary)
    # print(dataset)
    vecs = []

    for i in range(dataset.shape[0]):
        sentence = jieba.lcut(dataset[i][0])
        curVec = []
        for j in vocabulary:
            curVec.append(1 if j in sentence else 0)
        curVec.append(dataset[i, 2])
        curVec.append(s2l[dataset[i, 1]])
        vecs.append(curVec)
    vecs = np.array(vecs)
    # labels = np.array(dataset[:, 1]).reshape(vecs.shape[0], 1)
    # print(vocabulary)
    # print(vecs.shape)
    f = open('testT.txt', 'w')  # 产生数据集
    for i in vecs:
        f.write('\t'.join(i[:-2]) + '\t' + i[-1] + '\n')
    f.close()
    f = open('Tvec.txt', 'w')  # 词向量中每一位对应词
    f.write('\t'.join(vocabulary))
    f.close()
    for i in range(1, 8):
        tmpVec = [j[:-1] for j in vecs if j[-1] == str(i)]
        tmpVec = np.array(tmpVec)
        f = open('testT{}.txt'.format(i), 'w')
        for j in tmpVec:
            f.write('\t'.join(j) + '\n')
        f.close()


load()

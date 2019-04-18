import pickle
import random
import os

import jieba
import nltk
from django.conf import settings


class Bayes:
    def __init__(self):
        self.train_class = []
        self.stopwords = []
        self.train_data = []
        self.model_dir = os.path.join(settings.BASE_DIR, 'txtrobo', 'classifier', 'models', 'Bayes')

    """
        提取特征用于贝叶斯模型训练
    """

    def get_features(self, word):
        seg_list = jieba.cut_for_search(word)
        dict = {}
        for word in seg_list:
            if word not in self.stopwords:
                dict["has({})".format(word)] = word
        return dict

    """
        加载数据 [(句子,类别),...]
    """

    def load_data(self, data, classes):
        # ---从文件读取数据---现在改成从数据库读就注释吧
        # f = open(self.train_path)
        # data = f.readlines()
        # list = []
        # for line in data:
        #     x = line.split("\t")
        #     if x[1] not in self.train_class:
        #         self.train_class.append(x[1])  # 将所有类别保留 为最后的计算分类概率提供对比
        #     a = (x[0], x[1])
        #     list.append(a)
        self.train_data = data
        self.train_class = classes

    """
        加载停用词 格式为[停用词,...] 列表
    """

    def load_stop(self):
        # stopwords = [line.strip() for line in open(self.stopwords_path, 'r').readlines()]
        stopwords = ['嘿嘿', '呵呵']
        return stopwords

    """
        训练并保存模型
    """

    def train(self):
        # train_data = self.load_data()
        # print('traindata', train_data)
        if not self.train_data:
            print('请先load_data')
            return False
        random.shuffle(self.train_data)
        self.stopwords = self.load_stop()
        data = [(self.get_features(data), g) for (data, g) in self.train_data]
        # # 根据训练集比例划分数据
        # train_set,test_set = data[:int(len(data)*self.train_rate)],data[int(len(data)*self.train_rate):]
        classifier = nltk.NaiveBayesClassifier.train(data)
        with open(os.path.join(self.model_dir, 'my_classifier.pickle'), 'wb') as f:
            pickle.dump(classifier, f)
        with open(os.path.join(self.model_dir, 'classes.pickle'), 'wb') as f:
            pickle.dump(self.train_class, f)
        return True

    """
        使用模型，如果对于每个类的分类概率都小于50%，则拒绝回答
    """

    def use(self, word_input):
        ok = True

        with open(os.path.join(self.model_dir, 'my_classifier.pickle'), 'rb') as f:
            classifier = pickle.load(f)
        with open(os.path.join(self.model_dir, 'classes.pickle'), 'rb') as f:
            self.train_class = pickle.load(f)
        # 记录分类为每个类别的概率
        dic = {}
        for word in self.train_class:
            dic[word] = classifier.prob_classify(self.get_features(word_input)).prob(word)
        for key in dic:
            if dic[key] > 0.5:
                return ok, dic
        return not ok, dic


if __name__ == "__main__":
    classifier1 = Bayes()
    # classifier1.train_path = '../manualdata.txt'
    # classifier1.train()
    print(classifier1.use("你还"))

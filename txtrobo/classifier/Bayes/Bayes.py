import random
import nltk
import jieba
import pickle


class Bayes:
    def __init__(self):
        self.train_path = ''
        self.stopwords_path = ''
        self.train_class = []
        self.stopwords = ''
        self.train_data = []

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

    def load_data(self, data):
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
        random.shuffle(self.train_data)
        self.stopwords = self.load_stop()
        data = [(self.get_features(data), g) for (data, g) in self.train_data]
        train_set, test_set = data[:50], data[50:]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        # print(type(classifier))
        f = open('my_classifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()

    """
        使用模型，如果对于每个类的分类概率都小于50%，则拒绝回答
    """

    def use(self, word_input):

        f = open('my_classifier.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()
        # 记录分类为每个类别的概率
        dic = {}
        for word in self.train_class:
            dic[word] = classifier.prob_classify(self.get_features(word_input)).prob(word)
        for key in dic:
            if dic[key] > 0.5:
                return True
        return False


if __name__ == "__main__":
    classifier1 = Bayes()
    classifier1.train_path = '../manualdata.txt'
    classifier1.train()
    print(classifier1.use("Spring Boot 宇宙第一"))

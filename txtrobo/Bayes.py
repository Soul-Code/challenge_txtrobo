import random
import nltk
import jieba
import pickle
from . import models

class Bayes:
    train_path = ''
    stopwords_path = ''
    train_class = []
    stopwords = ''
    # train_rate = 0 #训练集比例


    """
        提取特征用于贝叶斯模型训练
    """
    def get_features(self,word):
        seg_list = jieba.cut_for_search(word)
        dict = {}
        for word in seg_list:
            if word not in self.stopwords:
                dict["has({})".format(word)] = word
        return dict

    """
        加载数据 [(句子,类别),...]
    """
    def load_data(self):
        f = open(self.train_path)
        data = f.readlines()
        list = []
        for line in data:
            x = line.split("\t")
            if x[1] not in self.train_class:
                self.train_class.append(x[1])  #将所有类别保留 为最后的计算分类概率提供对比
            a = (x[0], x[1])
            list.append(a)
        return list


    """
        加载停用词 格式为[停用词,...] 列表
    """
    def load_stop(self):
        stopwords = [line.strip() for line in open(self.stopwords_path, 'r').readlines()]
        return stopwords

    """
        训练并保存模型
    """
    def train(self):
        train_data = self.load_data()
        random.shuffle(train_data)
        self.stopwords = self.load_stop()
        data = [(self.get_features(data), g) for (data, g) in train_data]
        # # 根据训练集比例划分数据
        # train_set,test_set = data[:int(len(data)*self.train_rate)],data[int(len(data)*self.train_rate):]
        classifier = nltk.NaiveBayesClassifier.train(data)
        f = open('my_classifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()

    """
        使用模型，如果对于每个类的分类概率都小于50%，则拒绝回答
    """
    def use(self,word_input):

        f = open('classifier.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()
        # 记录分类为每个类别的概率
        dic = {}
        for word in self.train_class:
            dic[word] = classifier.prob_classify(self.get_features(word_input)).prob(word)
        print(dic)
        for key in dic:
            if dic[key] > 0.5:
                return True
        return False

if __name__ == "__main__":
    classifier1 = Bayes()
    # classifier1.train_rate = 0.7
    classifier1.train_path = 'manualdata.txt'
    classifier1.stopwords_path = '停用词.txt'
    classifier1.train()
    print(classifier1.use("Spring Boot 宇宙第一"))
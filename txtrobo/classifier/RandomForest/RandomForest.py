from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import jieba
import os

from django.conf import settings


class RFmodel:
    trainPath = ''
    testPath = ''
    PUNCTUATIONS = list('！!？?｡.＂"\'{}[]\\`~＃＄％＆＇（）()＊＋，-－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.')
    STOPWORDS = ['请问', '的', '吗', '是', '我', '呢', '啊']
    s2l = {'校车': '1', '校园网': '2', '银行、ATM': '3', '快递': '4', '打印店': '5', '在校事务': '6', '校医院': '7'}
    jieba.load_userdict('txtrobo/classifier/manualword.txt')

    def __init__(self):
        self.dictionary = []
        self.classes = []
        self.data = []
        self.model_forest1 = RandomForestClassifier()
        self.model_forest2 = {}
        self.model_dir = os.path.join(settings.BASE_DIR, 'txtrobo', 'classifier', 'models', 'RandomForest')

    """
    the file should be well constructed
    each line is a record split with '\t', the last column is the label
    if label not contained, need to tag manually
    """

    def load_data(self, classes, data):
        self.classes = classes
        self.data = data

    def train(self):
        self.dictionary, forest1, forest2 = self.transfer_data(self.data, self.classes)
        trainData = np.array(forest1)
        print(trainData)
        self.model_forest1.fit(trainData[:, :-1], trainData[:, -1])
        for key, value in forest2.items():
            value = np.array(value)
            print(value)
            model2 = RandomForestClassifier()
            model2.fit(value[:, :-1], value[:, -1])
            self.model_forest2[key] = model2

    def saveModel(self):
        with open(os.path.join(self.model_dir, 'classifier_forest1.pickle'), 'wb') as f:
            pickle.dump(self.model_forest1, f)
        with open(os.path.join(self.model_dir, 'classifier_forest2.pickle'), 'wb') as f:
            pickle.dump(self.model_forest2, f)
        with open(os.path.join(self.model_dir, 'classes.pickle'), 'wb') as f:
            pickle.dump(self.classes, f)
        with open(os.path.join(self.model_dir, 'dictionary.pickle'), 'wb') as f:
            pickle.dump(self.dictionary, f)

    def loadModel(self):
        with open(os.path.join(self.model_dir, 'classifier_forest1.pickle'), 'rb') as f:
            self.model_forest1 = pickle.load(f)
        with open(os.path.join(self.model_dir, 'classifier_forest2.pickle'), 'rb') as f:
            self.model_forest2 = pickle.load(f)
        with open(os.path.join(self.model_dir, 'classes.pickle'), 'rb') as f:
            self.classes = pickle.load(f)
        with open(os.path.join(self.model_dir, 'dictionary.pickle'), 'rb') as f:
            self.dictionary = pickle.load(f)

    """
    record is a string need to be classifyied
    """

    def preprocess(self, record):
        vec = []
        for word in self.dictionary:
            if word in record:
                vec.append(1)
            else:
                vec.append(0)
        return np.array(vec)

    def use(self, txt_in, flow=None):
        data = self.preprocess(txt_in)
        if flow is None:
            # 一层随机森林
            return self.model_forest1.predict([data])
            # 二层随机森林
        else:
            return self.model_forest2[flow.name].predict([data])
        # print(data)

    def transfer_data(self, data, classes):
        dataset = np.array(data)
        self.classes = classes
        # 获取词典
        vocabulary = []
        for i in range(dataset.shape[0]):
            vocabulary.extend(jieba.lcut(dataset[i][0]))
        vocabulary = set(vocabulary)
        # 移除标点符号
        for punc in self.PUNCTUATIONS:
            if punc in vocabulary:
                vocabulary.remove(punc)
        # 移除停用词
        for word in self.STOPWORDS:
            if word in vocabulary:
                vocabulary.remove(word)
        vocabulary = list(vocabulary)
        vecs = []

        for i in range(dataset.shape[0]):
            sentence = jieba.lcut(dataset[i][0])
            curVec = []
            for j in vocabulary:
                curVec.append(1 if j in sentence else 0)
            curVec.append(dataset[i, 2])
            curVec.append(dataset[i, 1])
            vecs.append(curVec)
        vecs = np.array(vecs)

        forest1 = []
        for i in vecs:
            forest1.append(np.append(i[:-2], i[-1]))

        forest2 = {}
        for _class in classes:
            class_data = [j[:-1] for j in vecs if j[-1] == _class]
            for j in class_data:
                if _class in forest2:
                    forest2[_class].append(j)
                else:
                    forest2[_class] = [j]
        return vocabulary, forest1, forest2


if __name__ == '__main__':
    model = RFmodel()

    classes = ['校车', '校园网', '银行、ATM', '快递', '打印店', '在校事务', '校医院']
    model.load_data(classes, 1)
    model.train()
    model.saveModel()
    record = '校车宝山校区'  # input()
    C1 = model.use(record)
    print(C1)
    # modelS = RFmodel()
    # modelS.trainPath = 'testT{}.txt'.format(int(C1))
    # modelS.train()
    # print(C1, ':', modelS.classify(record))
    # model.testPath = 'testT1.txt'
    # model.test()

    # model.manualTest()

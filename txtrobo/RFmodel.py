from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import jieba
from . import models

def manualLabel(dataset, label):
    for i in dataset:
        i.append(label)


class RFmodel:
    trainPath = ''
    testPath = ''
    clf = RandomForestClassifier()

    """
    the file should be well constructed
    each line is a record split with '\t', the last column is the label
    if label not contained, need to tag manually
    """

    def loadTrainSet(self):
        dataMat = []
        fr = open(self.trainPath)
        for line in fr.readlines():
            curLine = line.strip().split('\t')
            fltLine = list(map(float, curLine))
            dataMat.append(fltLine)
        return dataMat

    def loadTestSet(self):
        dataMat = []
        fr = open(self.testPath)
        for line in fr.readlines():
            curLine = line.strip().split('\t')
            fltLine = list(map(float, curLine))
            dataMat.append(fltLine)
        return dataMat

    def train(self):
        trainData = np.array(self.loadTrainSet())
        self.clf.fit(trainData[:, :-1], trainData[:, -1])

    def test(self):
        testData = np.array(self.loadTestSet())
        result = self.clf.predict(testData[:, :-1])
        print('%4s%4s' % ('实际', '预测'))
        for i in range(len(testData[:, -1])):
            print('%6s%6s' % (testData[i, -1], result[i]))

    def manualTest(self):
        dataset = ['校车什么时候发车？', '校医院能拔牙吗？', '新世纪快递点在哪里？', '我要取现。', '校园网信号差！']
        f = open('Tvec.txt')
        string = f.readlines()[0].strip().split('\t')
        f.close()
        vecs = []
        for data in dataset:
            curVec = []
            for s in string:
                curVec.append(1 if s in data else 0)
            vecs.append(curVec)
        vecs = np.array(vecs)
        print(self.clf.predict(vecs))

    def saveModel(self, file):
        f = open(file, 'wb')
        pickle.dump(self.clf, f)
        f.close()

    def loadModel(self, file):
        f = open(file, 'rb')
        self.clf = pickle.load(f)
        f.close()

    """
    record is a string need to be classifyied
    """

    def preprocess(self, record):
        vec = []
        f = open('Tvec.txt')
        wordsStored = []
        for i in f.readlines():
            wordsStored.extend(i.split('\t'))
        f.close()
        for word in wordsStored:
            if word in record:
                vec.append(1)
            else:
                vec.append(0)
        return np.array(vec)

    def classify(self, record):
        data = self.preprocess(record)
        # print(data)
        return self.clf.predict([data])


model = RFmodel()
# model.trainPath = 'dataRF.txt'
# model.train()
# model.saveModel('RFM.dat')
# model.loadModel('RFM.dat')
# model.testPath = 'dataRT.txt'
# model.test()

model.trainPath = 'testT.txt'
model.train()
record = '校车宝山校区'  # input()
C1 = model.classify(record)
modelS = RFmodel()
modelS.trainPath = 'testT{}.txt'.format(int(C1))
modelS.train()
print(C1, ':', modelS.classify(record))
# model.testPath = 'testT1.txt'
# model.test()

# model.manualTest()

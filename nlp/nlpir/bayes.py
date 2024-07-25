import random
import re

import numpy as np
import pandas as pd


def loadDataSet(filename):
    data = pd.read_csv(filename)
    postingList = []
    for sentence in data['short']:
        word = sentence.strip().split()
        postingList.append(word)

    classVec = data['sentiment'].values.tolist()
    return postingList, classVec


def createVocbList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec


def getMat(inputSet):
    trainMat = []
    vocabList = createVocbList(inputSet)
    for Set in inputSet:
        trainMat.append(setOfWords2Vec(vocabList, Set))
    return trainMat


def trainNB(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    #计算词条出现的概率
    p1Vect = np.log(p1Num / p1Denom)
    p0Vect = np.log(p0Num / p0Denom)
    return p1Vect, p0Vect, pAbusive


def calc_prob(data_file_path):
    train_postingList, train_classVec = loadDataSet(data_file_path)
    vocabSet = createVocbList(train_postingList)
    trainMat = getMat(train_postingList)
    p1V, p0V, PAb = trainNB(trainMat, train_classVec)
    return {
        "vocabSet": vocabSet,
        "p1V": p1V.tolist(),
        "p0V": p0V.tolist(),
        "PAb": PAb
    }


def classifyNB(ClassifyVec, p1V, p0V, pAb):
    #将对应元素相乘
    p1 = sum(ClassifyVec * p1V) + np.log(pAb)
    p0 = sum(ClassifyVec * p0V) + np.log(1.0 - pAb)
    print(p1, p0)
    if p1 > p0:
        return 1
    else:
        return 0


def get_classify(target_text, vocabSet, p1V, P0V, PAb):
    testVec = setOfWords2Vec(vocabSet, target_text)
    return 1 if classifyNB(testVec, np.array(p1V), np.array(P0V), PAb) else 0


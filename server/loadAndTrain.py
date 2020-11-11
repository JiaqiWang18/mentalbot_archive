import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import json
import pickle

def loadAndGetTrainData(path):
    with open(path) as file:
        data = json.load(file)

    words = []
    labels = []
    docs_x = []
    docs_y = []

    for each_dic in data:
        print(each_dic)
        for pattern in each_dic["match"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(each_dic["tag"])

        if each_dic["tag"] not in labels:
            labels.append(each_dic["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]
    print("first loop done")
    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("trainDataAndModel/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
    print(len(output))
    print(output[0])
    #print(output[0])

def trainModel(path):
    with open(path, "rb") as f:
        words, labels, training, output = pickle.load(f)
    tensorflow.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 128)
    net = tflearn.fully_connected(net, 128)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    print(training)
    print(output)
    model.fit(training, output, n_epoch=100, batch_size=8, show_metric=True)
    model.save("trainDataAndModel/model.tflearn")

if __name__ == "__main__":
    loadAndGetTrainData("tags.json")
    trainModel('trainDataAndModel/data.pickle')


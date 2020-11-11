from nltk.stem.lancaster import  LancasterStemmer
from tflearn import input_data
from tflearn import fully_connected
from tflearn import DNN
from tflearn import regression
import nltk
import numpy
import random
import json
import pickle

stemmer = LancasterStemmer()

print("loading complete")

def getIntent(path):
    try:
        with open(path) as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"{path} not found")

def getData(dataPath):
    try:
        with open(dataPath, "rb") as f:
            words, labels, training, output = pickle.load(f)
        return [words,labels,training,output]
    except FileNotFoundError:
        raise FileNotFoundError(f"{dataPath} not found")


def getModel(dataPath):

    data = getData(dataPath)
    output = data[3]
    training = data[2]

    net = input_data(shape=[None, len(training[0])])
    net = fully_connected(net, 128)
    net = fully_connected(net, 128)
    net = fully_connected(net, len(output[0]), activation="softmax")
    net = regression(net)

    model = DNN(net)

    return model

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def test_chat(modelPath,dataPath,intentPath):
    model = getModel(dataPath)
    try:
        model.load(modelPath)
    except FileNotFoundError:
        raise FileNotFoundError(f"{modelPath} not found")
    print("___________________")
    print("model loaded")
    intents = getIntent(intentPath)

    rd = getData(dataPath)
    words = rd[0]
    labels = rd[1]

    print("Start talking with the bot (type q to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "q":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        print(results)
        if results[results_index] > 0.5:

            for tg in intents:
                if tg['tag'] == tag:
                    responses = tg['response']
            print(random.choice(responses))
        else:
            print("Please elaborate")

def chat(modelPath,dataPath,intentPath,user_input):
    model = getModel(dataPath)
    try:
        model.load(modelPath)
    except FileNotFoundError:
        raise FileNotFoundError(f"{modelPath} not found")
    print("___________________")
    print("model loaded")
    intents = getIntent(intentPath)

    rd = getData(dataPath)
    words = rd[0]
    labels = rd[1]

    results = model.predict([bag_of_words(user_input, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index] > 0.5:

        for tg in intents:
            if tg['tag'] == tag:
                responses = tg['response']
        return random.choice(responses)
    else:
        return "Please elaborate"

if __name__=="__main__":
    test_chat('trainDataAndModel/model.tflearn','trainDataAndModel/data.pickle','tags.json')
    #print(chat('trainDataAndModel/model.tflearn','trainDataAndModel/data.pickle','tags.json',"hello"))

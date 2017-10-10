

import transition
import conll
import dparser
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import linear_model
from sklearn import datasets
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.grid_search import GridSearchCV
import pickle

def encode_classes(y_symbols):
    """
    Encode the classes as numbers
    :param y_symbols:
    :return: the y vector and the lookup dictionaries
    """
    # We extract the chunk names
    classes = sorted(list(set(y_symbols)))

    # We assign each name a number
    dict_classes = dict(enumerate(classes))


    # We build an inverted dictionary
    inv_dict_classes = {v: k for k, v in dict_classes.items()}


    # We convert y_symbols into a numerical vector
    y = [inv_dict_classes[i] for i in y_symbols]
    return y, dict_classes, inv_dict_classes

def extract_features(sentences, feature_names):
    """
    Builds X matrix and y vector
    X is a list of dictionaries and y is a list
    :param sentences:
    :param w_size:
    :return:
    """
    X_l = []
    y_l = []
    for sentence in sentences:
        X, y = extract_features_sent(sentence, feature_names)
        X_l.extend(X)
        y_l.extend(y)
    return X_l, y_l



def extract_features_sent(sentence, feature_names):
    """
    Extract the features from one sentence
    returns X and y, where X is a list of dictionaries and
    y is a list of symbols
    :param sentence:
    :param w_size:
    :return:
    """
    #sentence  = sentence.splitlines()

    stack = []
    graph = {}
    queue = list(sentence)
    graph['heads'] = {}
    graph['heads']['0'] = '0'
    graph['deprels'] = {}
    graph['deprels']['0'] = 'ROOT'

    transitions = []

    x = list()
    X = list()
    y = list()
    while queue:
        if (len(stack) > 0):
            x.append(stack[0]['cpostag'])
            x.append(stack[0]['form'])
        else:
            x.append('nil')
            x.append('nil')

        if (queue):
            x.append(queue[0]['cpostag'])
            x.append(queue[0]['form'])
        else:
            x.append('nil')
            x.append('nil')

        x.append(transition.can_reduce(stack, graph))
        x.append(transition.can_leftarc(stack, graph))
        X.append(dict(zip(feature_names, x)))

        stack, queue, graph, trans = dparser.reference(stack, queue, graph)
        y.append(trans)
        x = list()
    #stack, graph = transition.empty_stack(stack, graph)


    #for word in queue:
        #print(word['form'])
        #stack, queue, graph, trans = reference(stack, queue, graph)
        #transitions.append(trans)
       # stack, graph = transition.empty_stack(stack, graph)
    return X, y


if __name__ == '__main__':
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)
    feature_names = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-la',
                     'can-re']
    X_dict, y_dict = extract_features(formatted_corpus, feature_names)
    print(X_dict)
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_dict)

    y, dict_classes, inv_dict_classes = encode_classes(y_dict)

    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear', verbose=1)
    model = classifier.fit(X, y)
    pickle.dump(classifier, open("model1.pkl", "wb"))
    pickle.dump(dict_classes, open("dict_classes1.pkl", "wb"))
    pickle.dump(vec, open("vec1.pkl", "wb"))
    print(model)
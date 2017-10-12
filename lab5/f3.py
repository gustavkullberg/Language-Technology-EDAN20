import transition
import conll
import dparser
import pickle

import time
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.grid_search import GridSearchCV

def extract_features(sentences, feature_names):
    """
    Builds X matrix and y vector
    X is a list of dictionaries and y is a list
    :param sentences:
    :param feature_names:
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
    :param feature_names
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
    d=len(sentence)


    while queue:

        if (len(stack) > 0):
            x.append(stack[0]['cpostag'])
        else:
            x.append('nil')
        if(len(stack)>1):
            x.append(stack[1]['cpostag'])
        else:
            x.append('nil')
        if (len(stack) > 0):
            x.append(stack[0]['form'])
        else:
            x.append('nil')
        if(len(stack)>1):
            x.append(stack[1]['form'])
        else:
            x.append('nil')
        if(queue):
            x.append(queue[0]['cpostag'])
        else:
            x.append('nil')
        if(len(queue)>1):
            x.append(queue[1]['cpostag'])
        else:
            x.append('nil')
        if(queue):
            x.append(queue[0]['form'])
        else:
            x.append('nil')
        if (len(queue)> 1):
            x.append(queue[1]['form'])
        else:
            x.append('nil')


        x.append(transition.can_reduce(stack, graph))
        x.append(transition.can_leftarc(stack, graph))

        if (len(stack) > 0):
            if stack[0]['form']=='ROOT':
                x.append('nil')
                x.append('nil')
            else:
                x.append(sentence[int(stack[0]['id'])-1]['form'])
                x.append(sentence[int(stack[0]['id'])-1]['cpostag'])
            if int(stack[0]['id'])== d-1:
                x.append('nil')
                x.append('nil')
            else:
                x.append(sentence[int(stack[0]['id'])+1]['form'])
                x.append(sentence[int(stack[0]['id'])+1]['cpostag'])
        else:
            x.append('nil')
            x.append('nil')
            x.append('nil')
            x.append('nil')

        X.append(dict(zip(feature_names, x)))
        stack, queue, graph, trans = dparser.reference(stack, queue, graph)
        y.append(trans)
        x = list()
       # x.append(stack[0]['cpostag'])


    return X, y


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


if __name__ == '__main__':
    # train_file = 'swedish_talbanken05_train.conll'
    # test_file = 'swedish_talbanken05_test_blind.conll'
    # column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    # column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    #
    # sentences = conll.read_sentences(train_file)
    # formatted_corpus = conll.split_rows(sentences, column_names_2006)
    #
    # feature_names = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS', 'queue0_word', 'queue1_word', 'can-re',
    #                  'can-la','before_word', 'before_POS', 'after_word', 'after_POS']
    # X, y = extract_features(formatted_corpus, feature_names)
    #
    # for i in range(9):
    #     print(str(X[i]) + " " + str(y[i]))

    start_time = time.clock()
    train_corpus = 'swedish_talbanken05_train.conll'
    test_corpus = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    feature_names = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS',
                     'queue0_word', 'queue1_word', 'can-re',
                     'can-la', 'before_word', 'before_POS', 'after_word', 'after_POS']

    train_sentences = conll.read_sentences(train_corpus)
    formatted_corpus = conll.split_rows(train_sentences, column_names_2006)

    print("Extracting the features...")
    X_dict, y_symbols = extract_features(formatted_corpus, feature_names)

    print("Encoding the features and classes...")
    # Vectorize the feature matrix and carry out a one-hot encoding
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_dict)
    # The statement below will swallow a considerable memory
    # X = vec.fit_transform(X_dict).toarray()
    # print(vec.get_feature_names())

    y, dict_classes, inv_dict_classes = encode_classes(y_symbols)

    training_start_time = time.clock()
    print("Training the model...")
    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear', verbose=1)
    model3 = classifier.fit(X, y)

    pickle.dump(model3, open('model3','wb'))
    pickle.dump(vec,open('vec3', 'wb'))


    m3=pickle.load(open('model3','rb'))
    vec3 = pickle.load(open('vec3','rb'))

    test_start_time = time.clock()
    # We apply the model to the test set

    #train_sentences = list(conll.read_sentences(train_corpus))
    #formatted_corpus = conll.split_rows(train_sentences, column_names_2006)

    # Here we carry out a chunk tag prediction and we report the per tag error
    # This is done for the whole corpus without regard for the sentence structure
    print("Predicting the chunks in the train set...")
    #X_test_dict, y_test_symbols = extract_features(formatted_corpus, feature_names)
    # print(X_test_dict)
    # print(y_test_symbols)
    # Vectorize the test set and one-hot encoding
    #X_test = vec.transform(X_test_dict)  # Possible to add: .toarray()
    #y_test = [inv_dict_classes[i] if i in y_symbols else 0 for i in y_test_symbols]
    #y_test_predicted = classifier.predict(X_test)

    y_test_predicted = classifier.predict(X)

    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y, y_test_predicted)))

    # Here we tag the test set and we save it.
    # This prediction is redundant with the piece of code above,
    # but we need to predict one sentence at a time to have the same
    # corpus structure
    print("Predicting the test set...")
    #f_out = open('out', 'w')
    #predict(test_sentences, feature_names, f_out)

    end_time = time.clock()
    print("Training time:", (test_start_time - training_start_time) / 60)
    print("Test time:", (end_time - test_start_time) / 60)


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

def extract_features(sentences, feature_names, classifer, dict_classes,vec):

    X_l = []
    y_l = []
    for sentence in sentences:
        X, y = extract_features_sent(sentence, feature_names, classifier, dict_classes, vec)
        X_l.extend(X)
        y_l.extend(y)
    return X_l, y_l


def parse_ml(stack, queue, graph, trans):
    if stack and trans[:2] == 'ra':
        stack, queue, graph = transition.right_arc(stack, queue,graph, trans[3:])
        return stack, queue, graph, 'ra'
    if stack and trans[:2] == 'la':
        stack, queue, graph = transition.left_arc(stack, queue, graph,trans[3:])
        return stack, queue, graph, 'la'

def extract_features_sent(sentence, feature_names, classifier, dict_classes, vec):

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
        #remove reference, predict what action should be done(equiv to trans)
        trans_nr[0] = classifier.predict(vec.fit_transform(X))

        stack, queue, graph = parse_ml(stack, queue, graph, trans_nr[0])
        x = list()
    #stack, graph = transition.empty_stack(stack, graph)

    transition.empty_stack(stack, graph)
    for word in sentence:
        #Set the words
    word['head'] = graph['heads'][word['id']]
    #do cooreespomdoing for deprels


    return X

if __name__ == '__main__':
    test_file = 'swedish_talbanken05_test_blind.conll'
    sentences = conll.read_sentences(test_file)
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    formatted_corpus = conll.split_rows(sentences, column_names_2006_test)
    feature_names = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-la',
                     'can-re']

    classifier = pickle.load( open('model1.pkl', 'rb'))
    print(classifier)
    dict_classes = pickle.load( open('dict_classes1.pkl','rb'))
    vec = pickle.load(open ('vec1.pkl', 'rb'))
    print(vec)
    X_dict, y_dict = extract_features(formatted_corpus, feature_names, classifier, dict_classes, vec)

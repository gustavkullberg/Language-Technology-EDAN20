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
        X = extract_features_sent(sentence, feature_names, classifier, dict_classes, vec)
        X_l.extend(X)
        #y_l.extend(y)
    return X_l, y_l


def parse_ml(stack, queue, graph, trans):

    if stack and trans[:2] == 'ra':
        stack, queue, graph = transition.right_arc(stack, queue,graph, trans[3:])
        return stack, queue, graph, 'ra'
    if stack and trans[:2] == 'la':
        stack, queue, graph = transition.left_arc(stack, queue, graph,trans[3:])
        return stack, queue, graph, 'la'
    if trans == 're':
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    if trans == 'sh':
        stack, queue, graph = transition.shift(stack, queue, graph)
        return stack, queue, graph, 'sh'

    print(trans, "is not a valid action")

    return None

def extract_features_sent(sentence, feature_names, classifier, dict_classes, vec):

    stack = []
    graph = {}
    queue = list(sentence)
    graph['heads'] = {}
    graph['heads']['0'] = '0'
    graph['deprels'] = {}
    graph['deprels']['0'] = 'ROOT'

    x = list()
    X = list()
    d = len(sentence)
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
        X = (dict(zip(feature_names, x)))
        trans_nr = classifier.predict(vec.transform(X))[0]
        trans = dict_classes[trans_nr]
        stack, queue, graph, trans = parse_ml(stack, queue, graph, trans)
        x = list()

    transition.empty_stack(stack, graph)
    for word in sentence:
        word['head'] = graph['heads'][word['id']]
        word['deprel'] = graph['deprels'][word['id']]
    return X

if __name__ == '__main__':
    test_file = 'swedish_talbanken05_test_blind.conll'
    sentences = conll.read_sentences(test_file)
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    formatted_corpus = conll.split_rows(sentences, column_names_2006)
    feature_names = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS', 'queue0_word', 'queue1_word', 'can-re',
                     'can-la','before_word', 'before_POS', 'after_word', 'after_POS']
    classifier = pickle.load( open('model3.pkl', 'rb'))
    #print(classifier)
    dict_classes = pickle.load( open('dict_classes3.pkl','rb'))
    vec = pickle.load(open ('vec3.pkl', 'rb'))
    #print(vec)
    X_dict, y_dict = extract_features(formatted_corpus, feature_names, classifier, dict_classes, vec)
    conll.save("parsedTestSentences3", formatted_corpus, column_names_2006)

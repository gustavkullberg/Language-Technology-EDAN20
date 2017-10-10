

import transition
import conll
import dparser

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
    print('this is queue',queue)
    graph['heads'] = {}
    graph['heads']['0'] = '0'
    graph['deprels'] = {}
    graph['deprels']['0'] = 'ROOT'

    transitions = []

    x = list()
    while queue:
        stack, queue, graph, trans = reference(stack, queue, graph)
        transitions.append(trans)
    stack, graph = transition.empty_stack(stack, graph)


    #for word in queue:
        #print(word['form'])
        #stack, queue, graph, trans = reference(stack, queue, graph)
        #transitions.append(trans)
       # stack, graph = transition.empty_stack(stack, graph)
    X = 0
    y = 0

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
    extract_features(formatted_corpus, feature_names)
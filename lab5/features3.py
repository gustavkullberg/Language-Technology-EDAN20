import transition
import conll
import dparser

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


        X.append(x)
        stack, queue, graph, trans = dparser.reference(stack, queue, graph)
        y.append(trans)
        x = list()
       # x.append(stack[0]['cpostag'])


    return X, y



if __name__ == '__main__':
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    feature_names = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS', 'queue0_word', 'queue1_word', 'can-re',
                     'can-la','before_word', 'before_POS', 'after_word', 'after_POS']
    X, y = extract_features(formatted_corpus, feature_names)
    for i in range(9):
        print(str(X[i]) + " " + str(y[i]))
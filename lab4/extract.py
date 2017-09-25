import conll

if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    train_corpus = 'swedish_talbanken05_train.conll'
    train_sentences = conll.read_sentences(train_corpus)
    formatted_corpus = conll.split_rows(train_sentences, column_names_2006)
    Count = 0
    pairDict = {}
    verbDict ={}
    subDict = {}
    for i in range(len(formatted_corpus)):
        for j in range(len(formatted_corpus[i])):
            if(formatted_corpus[i][j]['cpostag'] == 'VV'):
                    for k in range(len(formatted_corpus[i])):
                            if(formatted_corpus[i][k]['deprel'] == 'SS'):
                                verb = formatted_corpus[i][j]['form']
                                sub = formatted_corpus[i][k]['form']
                                verbSubPair = (verb, sub)
                                if(verbSubPair in pairDict):
                                    pairDict[verbSubPair] += 1
                                    Count+=1
                                else:
                                    pairDict[verbSubPair] = 1

    sor = sorted(pairDict, key = pairDict.get, reverse=True)

    for i in range(5):
        print(sor[i])
    print(Count)
    print(pairDict[('finns','som')])
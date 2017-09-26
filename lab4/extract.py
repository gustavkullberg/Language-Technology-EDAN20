import conll

if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    train_corpus = 'swedish_talbanken05_train.conll'
    train_sentences = conll.read_sentences(train_corpus)
    formatted_corpus = conll.split_rows(train_sentences, column_names_2006)
    Count = 0
    pairDict = {}
    for i in range(len(formatted_corpus)):
        for j in range(len(formatted_corpus[i])):
            if(formatted_corpus[i][j]['deprel'] == 'SS'):
                sub = formatted_corpus[i][j]['form'].lower()
                verb = formatted_corpus[i][int(formatted_corpus[i][j]['head'])]['form'].lower()
                verbSubPair = (verb, sub)
                Count += 1
                if (verbSubPair in pairDict):
                    pairDict[verbSubPair] += 1
                else:
                    pairDict[verbSubPair] = 1

    sor = sorted(pairDict, key = pairDict.get, reverse=True)


    for i in range(5):
        print(sor[i])
        print(pairDict[sor[i]])
    print('In total ',Count, ' pairs')
    print('')
    Count = 0
    tripleDict = {}
    for i in range(len(formatted_corpus)):
        for j in range(len(formatted_corpus[i])):
            if (formatted_corpus[i][j]['deprel'] == 'SS'):
                sub = formatted_corpus[i][j]['form'].lower()
                verb = formatted_corpus[i][int(formatted_corpus[i][j]['head'])]['form'].lower()
                #verbSubPair = (verb, sub)
                for l in range(len(formatted_corpus[i])):
                    if(formatted_corpus[i][l]['deprel'] == 'OO' and int(formatted_corpus[i][l]['head']) == int(formatted_corpus[i][j]['head'])):
                        obj = formatted_corpus[i][l]['form'].lower()
                        verbSubObj = (verb, sub, obj)
                        Count += 1
                        if (verbSubObj in tripleDict):
                            tripleDict[verbSubObj] += 1
                        else:
                            tripleDict[verbSubObj] = 1
                        break



    sor = sorted(tripleDict, key=tripleDict.get, reverse=True)

    for i in range(5):
        print(sor[i])
        print(tripleDict[sor[i]])
    print('In total ', Count, ' triples')

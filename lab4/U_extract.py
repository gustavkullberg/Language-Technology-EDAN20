import conll

if __name__ == '__main__':
    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']
    #train_corpus = 'UD_Kazakh/kk-ud-train.conllu'
    #train_corpus = 'en-ud-train.conllu'
    train_corpus = 'UD_French/fr-ud-train.conllu'
    #train_corpus = 'ud-treebanks-conll2017/UD_Swedish/sv-ud-train.conllu'
    #train_corpus = 'swedish_talbanken05_train.conll'
    train_sentences = conll.read_sentences(train_corpus)
    formatted_corpus = conll.split_rows(train_sentences, column_names_u)
    newlist = []
    count = 0
    for i in range(len(formatted_corpus)):
        secondList = []
        for j in range(len(formatted_corpus[i])):
            if ('-' not in formatted_corpus[i][j]['id']):
                formatted_corpus[i][j][formatted_corpus[i][j]['id']] = formatted_corpus[i][j]
                secondList.append(formatted_corpus[i][j])
        newlist.append(secondList)

    Count = 0
    pairDict = {}
    for i in range(len(newlist)):
        for j in range(len(newlist[i])):
            if(newlist[i][j]['deprel'] == 'nsubj'):
                sub = newlist[i][j]['form'].lower()
                verb = newlist[i][int(newlist[i][j]['head'])]['form'].lower()
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
    for i in range(len(newlist)):
        for j in range(len(newlist[i])):
            if (newlist[i][j]['deprel'] == 'nsubj'):
                sub = newlist[i][j]['form'].lower()
                verb = newlist[i][int(newlist[i][j]['head'])]['form'].lower()
                for l in range(len(newlist[i])):
                    if(newlist[i][l]['deprel'] == 'obj' and int(newlist[i][l]['head']) == int(newlist[i][j]['head'])):
                        obj = newlist[i][l]['form'].lower()
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




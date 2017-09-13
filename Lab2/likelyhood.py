import sys
import math
import regex as re

def tokenize(text):
    words = re.findall("\p{L}+|<s>|</s>", text)
    return words

def getNbrOfSen(text):return len(re.findall(r'(\p{Lu}[^\.!?]*[\.!?])',text))

def tokenize1(text):
    sentences = re.findall(r'(\p{Lu}[^\.!?]*[\.!?])',text)
    fulltext = ""
    for w in range (len(sentences)):
        words = tokenize(sentences[w].lower())
        words = " "  .join(words)
        sentences[w] = '<s> ' + words + ' </s>'
    fulltext = " " .join(sentences)
    return tokenize(fulltext)

def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency,{k: v / len(words) for k,v in frequency.items()}


def count_bigrams(words, uni):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams,{k: v/len(bigrams) / (uni[k[0]]) for k,v in frequency_bigrams.items()}



if __name__ == '__main__':
    sen = 'Det var en gång en katt som hette Nils.'
    sen = tokenize1(sen)
    #sen = ['<s>'] + sen + ['</s>']
    text = sys.stdin.read()
    words = tokenize1(text)
    freq,uni = count_unigrams(words)
    print('Unigram Model')
    print('==========================')
    print('w C(w) #words P(w)')
    print('==========================')
    P=1
    entropy = 0;
    for w in sen:
        P = P*uni[w]
        entropy +=math.log2(uni[w])
        print(w+'\t', freq[w],'\t',len(words),'\t', uni[w])
    entropy = -(1/len(sen))*entropy
    print('Prob. unigrams: \t',P)
    print('Entropy: \t',entropy)
    print('Perplexity: \t', 2**(entropy))



    print('\nBigram Model')
    print('==========================')
    print('wi wi+1 Ci,i+1 C(i) P(wi+1|wi)')
    print('==========================')
    freqbi,bi = count_bigrams(words, uni)
    P=1
    entropy=0;
    for i in range(len(sen)-1):
        tuppi = (sen[i], sen[i+1])
        biProb = bi.get(tuppi, None)
        if(biProb == None):
            biProb = uni[sen[i+1]]
            print(tuppi, '\t', 0,'\t',freq[sen[i]],'\t' ,' *backoff', biProb)
        else:print(tuppi, '\t',freqbi[tuppi],'\t',freq[sen[i]],'\t', biProb)
        entropy += math.log2(biProb)
        P=P*biProb
    entropy = -(1 / (len(sen)-1) * entropy)
    print('Prob. bigrams: \t', P)
    print('Entropy: ', entropy)
    print('Perplexity: ', 2**entropy)






import sys
import regex as re
import pickle
import os
import numpy

def words(text): return re.finditer(r'\p{L}+', text.lower())

def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

def createDictionaries(files):
    dictionaries = {}
    words_per_doc = {}
    for f in files:
        count = 0
        WORDS = (words(open(arg + '/' + f).read()))
        for w in WORDS:
            print(w.start())
            dictionaries.setdefault(w.group(), {}).setdefault(f, []).append(w.start())
            count += 1
        words_per_doc[f] = count

    tf_idf = dict()
    default = []
    for f in files:
        for w in dictionaries.keys():
            tf = len(dictionaries.get(w, default).get(f, default)) / words_per_doc[f]
            idf = numpy.log10(len(dictionaries[w]) / len(files))
            tf_idf.setdefault(f, {}).setdefault(w, -tf * idf)
    return tf_idf

def compareDocuments(dic, files):
    length = len(files)
    compareMatrix = numpy.zeros((length, length))
    mostSimilar = ['name1', 'name2', 0]
    for i in range(length):
        for j in range(length):
            nominator = denominator1 = denominator2 = 0
            for k in (dic[files[0]].keys()):
                nominator += dic[files[i]][k] * dic[files[j]][k]
                denominator1 += numpy.square(dic[files[i]][k])
                denominator2 += numpy.square(dic[files[j]][k])
            denominator = numpy.sqrt(denominator1 * denominator2)
            compareMatrix[i][j] = nominator / denominator
            if(mostSimilar[2] < compareMatrix[i][j] and compareMatrix[i][j] != 1):
                mostSimilar[0] = files[i]
                mostSimilar[1] = files[j]
                mostSimilar[2] = compareMatrix[i][j]
    print(compareMatrix)
    print(mostSimilar)


def main(arg):
    files = get_files(arg, 'txt')
    tf_idf = createDictionaries(files)
    for key in tf_idf.keys():
        print(key)
        for l in tf_idf[key].keys():
            print(l + '     ' + str(tf_idf[key][l]))
    compareDocuments(tf_idf, files)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        main(arg)

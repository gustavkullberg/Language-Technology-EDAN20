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

def main(arg):
    files = get_files(arg, 'txt')
    master_d = dict()
    dics = {}
    master_counts = {}
    for f in files:
        count = 0
        WORDS = (words(open(arg + '/' + f).read()))
        for w in WORDS:
            dics.setdefault(w.group(), {}).setdefault(f, []).append(w.start())
            count +=1
        master_counts[f] = count

    master_d = dict()
    default=[]
    for f in files:
        for w in dics.keys():
            tf = len(dics.get(w, default).get(f, default))/master_counts[f]
            idf = numpy.log10(len(dics[w])/len(files))
            master_d.setdefault(f, {}).setdefault(w, -tf*idf)


 #   for key in master_d.values():
  #      for l in key.keys():
   #         print(l + '     ' + str(key[l]))

    for key in master_d.keys():
        print(key)
        for l in master_d[key].keys():
            print(l + '     ' + str(master_d[key][l]))

    length = len(files)
    compareMatrix = numpy.zeros((length,length))
    for i in range(0, length):
        for j in range(0, length):
            nominator = denominator1 = denominator2 = 0
            for k in (master_d[files[0]].keys()):
                nominator += master_d[files[i]][k]*master_d[files[j]][k]
                denominator1+= numpy.square(master_d[files[i]][k])
                denominator2+= numpy.square(master_d[files[j]][k])
            denominator = numpy.sqrt(denominator1*denominator2)
            compareMatrix[i][j] = nominator/denominator
    print(compareMatrix)




        #compareMatrix[i][j] =




if __name__ == "__main__":
    for arg in sys.argv[1:]:
        main(arg)
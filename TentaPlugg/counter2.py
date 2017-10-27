import sys
import regex as re
import os


def getFiles(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if(file.endswith(suffix)):
            files.append(file)
    return files

def tokenize(text):
    words = re.split('\P{L}+', text)
    words.remove('')
    words.sort()
    return words

def count(files):
    dick = {}
    words_per_doc = {}
    for f in files:
        count = 0
        text = open(f).read().lower()
        words = tokenize(text)
        for w in words:
            counter+=1
            dick.setdefault(w, {}).setdefault(f, )
        



    dick = dict()
    counter = 0
    for w in words:
        counter +=1
        if(w not in dick.keys()):
            dick[w]=1
        else:
            dick[w]+=1
    return dick, counter


def main(arg):
    files = getFiles(arg, 'txt')
# text = open('file.txt').read()
#   words = tokenize(text)
    dick, nbrOfWords = count(files)
    for d in dick.keys():
        print(d, dick[d]/nbrOfWords)

            
if __name__ == '__main__':
   for arg in sys.argv[1:]:
        main(arg)
        

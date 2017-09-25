
def getResult():
    k = open('out', 'r').read()
    s = k.split()
    print(len(k)) #boks
    print(len(s)) #ord
    word_cnt = 0
    correct = 0
    for i in range(int(len(s)/4)):
        word_cnt += 1
        if(s[i*4+2] == s[i*4+3]):
            correct += 1

    print(word_cnt)
    print(correct)
    print(correct/word_cnt)

if __name__ == '__main__':
    getResult()
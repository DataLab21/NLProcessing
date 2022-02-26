import re
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

###################################################################

def BIO(txt):

    sentence = []
    test = []
    strA = ['F','EA', 'EB', 'NA', 'NB', 'PA', 'PB']
    
    f = open(txt + '.txt','r')

    for line in f:
        countA = [0, 0, 0, 0, 0, 0, 0]
        count = 1

        for x in range(len(strA)):
            p = re.compile('(?<=\<'+strA[x]+'>)(.*?)(?=<\/' + strA[x] + '>)')

            L = list(line)
            for m in p.finditer(''.join(L)):

                cc = str(count) + 'X'*((m.span()[1]-m.span()[0])-1)

                test.append([L[m.span()[0]:m.span()[1]],cc, strA[x]])
                L[m.span()[0]:m.span()[1]] = cc
                count += 1

            line = ''.join(L)
            line = line.replace('<'+strA[x]+'>',' ').replace('</'+strA[x]+'>',' ').replace('  ',' ').rstrip().lstrip()

        splits = line.split(' ')

        for i in splits:
            b = [z[1] for z in test]

            if i in b:
                x = ''.join(test[b.index(i)][0]).split(' ')
                for j in range(len(x)):
                    if x[j] =='': continue

                    if x[j] in b:
                        a = '<B-' if countA[strA.index(test[b.index(x[j])][2])] == 0 else '<I-'
                        if ''.join(test[b.index(x[j])][0])!='':
                            sentence.append([''.join(test[b.index(x[j])][0]), a + test[b.index(x[j])][2]+ '>'])
                            countA[strA.index(test[b.index(x[j])][2])]+=1

                    else:
                        a = '<B-' if countA[strA.index(test[b.index(i)][2])] == 0 else '<I-'
                        sentence.append([x[j], a + test[b.index(i)][2]+ '>'] )
                        countA[strA.index(test[b.index(i)][2])]+=1
            else:
                sentence.append([i,'O'])
                countA = [0, 0, 0, 0, 0, 0, 0]

        if len(sentence) > 0:
            tagged_sentences.append(sentence)
            sentence = []
            test = []

###################################################################

from numpy.lib.function_base import kaiser
from google.colab import files
uploaded = files.upload()

name = ['강원도관광지 태깅', '경기도관광지 태깅', '서울관광지 태깅', '전남관광지 태깅', '전북관광지 태깅', '제주도관광지 태깅', '충남관광지 태깅']
tagged_sentences = []

for i in range(len(name)): BIO(name[i])

print("전체 샘플 개수: ", len(tagged_sentences))

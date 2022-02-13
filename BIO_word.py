import re
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# BIO 형태(어절) >> 음절은 str을 list 형태로 쪼개면 사용가능

def BIO(txt, one):

    sentence = []
    test = []

    f = open(txt + '.txt','r')


    strA = ['F','EA', 'EB', 'PA', 'PB', 'NA', 'NB']

    for line in f:
        if len(line)==0 or line.startswith(one):
            continue

        for x in range(7):
            p = re.compile('(?<=\<'+strA[x]+'>)(.*?)(?=<\/' + strA[x] + '>)')
            p_tag_list = p.findall(line)
            if p_tag_list != []: 
                for y in p_tag_list:
                    
                    a = 0
                    for z in y.split(' '):

                        test.append(z)
                        if a == 0: 
                            test.append("<B-"+strA[x]+">")
                            a += 1
                        else:
                            test.append("<I-"+strA[x]+">")


            line = line.replace('<'+strA[x]+'>',' ').replace('</'+strA[x]+'>',' ').replace('  ',' ').rstrip().lstrip()
                
        splits = line.split(' ')

        for k in splits:

            if k in test:
                sentence.append([k, test[test.index(k)+1]])
            else:
                sentence.append([k, 'O'])
            
        if len(sentence) > 0:
            tagged_sentences.append(sentence)
            sentence = []
            test = []


# 파일 불러오기(전남, 전북, 충남, 제주의 경우 태깅.txt 생성 오류)
# 태깅.txt 생성 오류 ISSUE는 파일 형식이 통일되지 않은 부분에서 발생

from numpy.lib.function_base import kaiser
from google.colab import files
uploaded = files.upload()

a = ['강원도관광지 태깅', '경기도관광지 태깅', '서울관광지 태깅']
b = ['[경포 해변(완)]','[가평쁘디프랑스_50개]','[광화문]']

tagged_sentences = []

for i in range(len(a)): BIO(a[i], b[i])

print("전체 샘플 개수: ", len(tagged_sentences))

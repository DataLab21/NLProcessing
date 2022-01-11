- 리뷰할 코드: 피쳐자동태깅.py
- 사용한 라이브러리: openpyxl, re, pandas
- 사용한 태그명: <F>, <PA>, <PB>, <NA>, <EA>, <EB>
  - <F>: 명사
  - <PA>: 서술어(1)
  - <PB>: 서술어(2)
  - <NA>: 부정어
  - <EA>: 강조어(1)
  - <EB>: 강조어(2)
- 사용된 알고리즘: search & replace

```python
import openpyxl as xl
import re				#정규표현식 지원 모듈
import pandas as pd

#명사
f_tag = '<F>'
f_tag2 = '</F>'

#서술어
pa_tag = '<PA>'		#명사 앞
pa_tag2 = '</PA>'	
pb_tag = '<PB>'		#명사 뒤
pb_tag2 = '</PB>'

#부정어
na_tag = '<NA>'
na_tag2 = '</NA>'
nb_tag = '<NA>'
nb_tag2 = '</NA>'

#강조어
ea_tag = '<EA>'
ea_tag2 = '</EA>'
eb_tag = '<EB>'
eb_tag2 = '</EB>'

# 태깅할 파일 제목 확장자 포함해서 입력
filename_for_tagging = '전북 관광지리뷰.xlsx'
# 태깅 끝나고 저장할 파일명을 확장자 포함해서 입력
#filename_for_saving = 'tagged_test_pd.xlsx'

filename_for_saving = filename_for_tagging[:-5] + ' 태깅.txt'
saving = open(filename_for_saving, 'w')

filename_for_errlog = filename_for_tagging[:-5] + ' 에러로그.txt'
errlog = open(filename_for_errlog, 'w')

wb = xl.load_workbook('./' + filename_for_tagging)	#태깅할 파일 wb

for i in range(0, len(wb.sheetnames)):	#반복문(시트개수)
    
    xlsx_sheet = wb[wb.sheetnames[i]]	#i번째 시트
    
    #태깅할 파일에서 i번째 시트를 읽어온 내용 df
    df = pd.read_excel('./' + filename_for_tagging, sheet_name=wb.sheetnames[i])
    
    #['문장']은 열을 의미
    df['문장'] = df['문장'].str.strip().copy()	#문장 공백제거 후 복사본
    df['문장'] = df['문장'].str.strip('\n').copy()	#줄넘김(\n) 제거 후 복사본
    
    #['Unnamed: 6']은 병합으로 인하여 열 이름으로 찾지 못함 >> 서술어
    df['Unnamed: 6'] = df['Unnamed: 6'].str.strip().copy()
    df['Unnamed: 6'] = df['Unnamed: 6'].str.strip('\n').copy()
    
    df = df.fillna(pd.NA).copy()	#결측값 채우기: 병합 시 내용이 없는 행에 NA 설정
    
    for j in range(1, df.shape[0] - 1):	#반복: 행의 수
        sent = df['문장'][j]
        n_str = df['수식관계/평점'][j]	#명사
        p_str = df['Unnamed: 6'][j]		#서술어
        neg_str = df['Unnamed: 7'][j]	#부정어
        emph_str = df['Unnamed: 8'][j]	#강조어
        
        if n_str is not pd.NA:	#병합된 경우 첫번째 행만 실행됨
            try:

                #re.search(): 문자열 전체를 검색하여 정규식과 매치되는지 조사한다.
                #re.search().span(): 매치된 문자열의 (시작, 끝)에 해당하는 튜플을 돌려준다. 
                find = re.search(r'' + n_str.replace(' ', '*.'), str(sent)).span()
                
                #slice_replace(start, stop, repl): start와 stop사이에 replace
                df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], f_tag + n_str + f_tag2)[j]
                n_start = find[0]
                sent = df['문장'][j]

                find = re.search(r'' + p_str.replace(' ', '*.'), str(sent)).span()
                p_start = find[0]
                if find[0] > n_start:
                    df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], pb_tag + p_str + pb_tag2)[j]
                    sent = df['문장'][j]
                elif find[0] < n_start:
                    df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], pa_tag + p_str + pa_tag2)[j]
                    sent = df['문장'][j]
                check = j + 1
				
                while df['문장'][check] is pd.NA:
                    p_str = df['Unnamed: 6'][check]
                    next_find = re.search(r'' + p_str.replace(' ', '*.'), str(sent)).span()

                    if find[0] > n_start:
                        df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], pb_tag + p_str + pb_tag2)[j]
                        sent = df['문장'][j]
                    elif find[0] < n_start:
                        df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], pa_tag + p_str + pa_tag2)[j]
                        sent = df['문장'][j]

                    sent = df['문장'][j]
                    check += 1
                                
            except AttributeError:
                errlog.write(str(j) + "행 부근에서 에러 발생\n")

        elif n_str is pd.NA:
            continue
    
        if neg_str is not pd.NA:
            try:
                find = re.search(r'' + neg_str, str(sent)).span()

                if p_start > find[0]:
                    df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], nb_tag + neg_str + nb_tag2)[j]
                    sent = df['문장'][j]
                else:
                    df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], na_tag + neg_str + na_tag2)[j]
                    sent = df['문장'][j]

            except AttributeError:
                errlog.write(str(j) + "행 부근 부정어 없음?\n")

        if emph_str is not pd.NA:
            try:
                find = re.search(r'' + emph_str, str(sent)).span()

                if p_start > find[0]:
                    df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], eb_tag + emph_str + eb_tag2)[j]
                    sent = df['문장'][j]
                else:
                    df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], ea_tag + emph_str + ea_tag2)[j]
                    sent = df['문장'][j]
            except AttributeError:
                errlog.write(str(j) + "행 부근 강조어 없음?\n")
            

        if type(sent) is str:
            xlsx_sheet['L' + str(j + 2)] = sent
            
wb.save('./' + filename_for_saving)
print("태깅 끝 에러로그를 확인해주세요")
```



### 수정내용(01/11)

1. 태깅 내용이 엑셀 파일로 저장됨 >> **텍스트 파일**로 변경
2. 여러가지 수식관계에 대한 태깅이 실행되지 않음 >> **해결**
3. 마지막 문장에 대한 태깅이 이루어지지 않음 >> **해결**
4. 태깅 텍스트가 잘림 >> **해결**
5. 중복된 태그에 관하여 하나에 대해서만 태깅이 됨 >> **해결 못함**



```python
import openpyxl as xl
import re
import pandas as pd
import Function

#리스트
df_list = ['문장', '수식관계/평점', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']
str_list = ['','','','','']
tag_list = [['<FA>', '</FA>'],['PA','PB'],['NA','NB'],['EA','EB']]

#태깅할 파일 제목 확장자 포함해서 입력
filename_for_tagging = '서울관광지.xlsx'

filename_for_saving = filename_for_tagging[:-5] + ' 태깅.txt'
saving = open(filename_for_saving, 'w')

filename_for_errlog = filename_for_tagging[:-5] + ' 에러로그.txt'
errlog = open(filename_for_errlog, 'w')

wb = xl.load_workbook('./' + filename_for_tagging)

###Code
for i in range(0, len(wb.sheetnames)):
    
    if i == 0:
        saving_str = "[" + wb.sheetnames[i] + "]"
    else:
        saving_str = saving_str + "\n[" + wb.sheetnames[i] + "]"

    df = pd.read_excel('./' + filename_for_tagging, sheet_name=wb.sheetnames[i])

    for j in df_list:
        df[j] = df[j].str.strip().copy()
        df[j] = df[j].str.strip('\n').copy()
        
    df = df.fillna(pd.NA).copy()

    for j in range(1, df.shape[0]):
        
        for k in range(len(df_list)):
            str_list[k] = df[df_list[k]][j]
        
        if str_list[2] is not pd.NA:
            Function.tagging(1, df_list, str_list, tag_list, j, df, errlog)
            
            if str_list[3] is not pd.NA:
                Function.tagging(2, df_list, str_list, tag_list, j, df, errlog)

            if str_list[4] is not pd.NA:
                Function.tagging(3, df_list, str_list, tag_list, j, df, errlog)
            
        elif str_list[1] is pd.NA:
            continue
        
        if type(str_list[0]) is str:
            print(str(j + 2) + "행 태깅: " + str_list[0])
            saving_str = saving_str + "\n" + str(j + 2) + "행 태깅: " + str_list[0]
                
saving.write(saving_str)
```

```python
import openpyxl as xl
import re
import pandas as pd

def tagging(num, df_list, str_list, tag_list, j, df, errlog):
    
        try:
                
            find = re.search(r'' + str_list[1].replace(' ', '*.'), str(str_list[0])).span()
            if num == 1: df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], tag_list[0][0] + str_list[1] + tag_list[0][1])[j]
            start = find[0]
            str_list[0] = df['문장'][j]
            
            find = re.search(r'' + str_list[num + 1].replace(' ', '*.'), str(str_list[0])).span()
            if find[0] > start:
                df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], "<" + tag_list[num][1] + ">" + str_list[num+1] + "</" + tag_list[num][1] + ">")[j]
                str_list[0] = df['문장'][j]
            elif find[0] < start:
                df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1], "<" + tag_list[num][0] + ">" + str_list[num+1] + "</" + tag_list[num][0] + ">")[j]
                str_list[0] = df['문장'][j]

            check = j
            if check != df.shape[0] - 1 :
                check = j + 1

            while df['문장'][check] is pd.NA:
                
                str_list[1] = df['수식관계/평점'][check]
                next_find = re.search(r'' + str_list[1].replace(' ', '*.'), str(str_list[0])).span()
                if num == 1: df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], tag_list[0][0] + str_list[1] + tag_list[0][1])[j]
                start = next_find[0]
                str_list[0] = df['문장'][j]

                str_list[num+1] = df[df_list[num+1]][check]
                next_find = re.search(r'' + str_list[num + 1].replace(' ', '*.'), str(str_list[0])).span()
                if next_find[0] > start:
                    df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], "<" + tag_list[num][1] + ">" + str_list[num+1] + "</" + tag_list[num][1] + ">")[j]
                    str_list[0] = df['문장'][j]
                elif next_find[0] < start:
                    df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], "<" + tag_list[num][0] + ">" + str_list[num+1] + "</" + tag_list[num][0] + ">")[j]
                    str_list[0] = df['문장'][j]

                str_list[0] = df['문장'][j]
                
                if check == df.shape[0] - 1:
                    break
                else:
                    check += 1
                    
        except AttributeError:
            errlog.write(str(j + 2) + "행 부근에서 에러 발생 <" + str(num) + ">번째 테스트\n")
```


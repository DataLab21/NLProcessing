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
filename_for_saving = 'tagged_test_pd.xlsx'

filename_for_errlog = filename_for_tagging[:-5] + ' 에러로그.txt'
errlog = open(filename_for_errlog, 'w')
wb = xl.load_workbook('./' + filename_for_tagging)	#태깅할 파일 wb

for i in range(0, len(wb.sheetnames)):	#반복문(시트개수)
    xlsx_sheet = wb[wb.sheetnames[i]]	#i번째 시트
    saving.write("[" + wb.sheetnames[i] + "]\n")	#시트명 작성
    
    #태깅할 파일에서 i번째 시트를 읽어온 내용 df
    df = pd.read_excel('./' + filename_for_tagging, sheet_name=wb.sheetnames[i])
    
    #['문장']은 열을 의미
    df['문장'] = df['문장'].str.strip().copy()	#문장 공백제거 후 복사본
    df['문장'] = df['문장'].str.strip('\n').copy()	#줄넘김(\n) 제거 후 복사본
    
    #['Unnamed: 6']은 병합으로 인하여 열 이름으로 찾지 못함 >> 서술어
    df['Unnamed: 6'] = df['Unnamed: 6'].str.strip().copy()
    df['Unnamed: 6'] = df['Unnamed: 6'].str.strip('\n').copy()
    
    ***
    
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
				
                """수정전
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
				"""
                
                #수정 후 >> 수정 이유: 한 문장의 여러개의 수식관계가 있는 경우가 제대로 만들어지지 않음
                while df['문장'][check] is pd.NA:	#여러개의 수식관계가 있는 경우 >> NA일 경우는 병합이므로

                    n_str = df['수식관계/평점'][check]
                    next_find = re.search(r'' + n_str.replace(' ', '*.'), str(sent)).span()
                    df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], f_tag + n_str + f_tag2)[j]
                    n_start = next_find[0]
                    sent = df['문장'][j]	#check가 아니라 j로 쓰는 이유: 바꿀 문장은 1개이다.
                    
                    p_str = df['Unnamed: 6'][check]
                    next_find = re.search(r'' + p_str.replace(' ', '*.'), str(sent)).span()

                    if next_find[0] > n_start:
                        df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], pb_tag + p_str + pb_tag2)[j]
                        sent = df['문장'][j]
                    elif next_find[0] < n_start:
                        df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], pa_tag + p_str + pa_tag2)[j]
                        sent = df['문장'][j]

                    sent = df['문장'][j]
                    
                    if check != df.shape[0] - 1:	#check가 행의 수보다 커지지 않도록 방지
                        check += 1	
                                
            except AttributeError:
                errlog.write(str(j) + "행 부근에서 에러 발생\n")

        elif n_str is pd.NA:
            continue
        
        """여기서부터 수정
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
            """

        if type(sent) is str:
            #xlsx_sheet['L' + str(j + 2)] = sent
            saving.write(str(j + 2) + "행 태깅: " + sent + "\n")
            
#wb.save('./' + filename_for_saving)
print("태깅 끝 에러로그를 확인해주세요")
```


import openpyxl as xl
import re
import pandas as pd

f_tag = '<F>'
f_tag2 = '</F>'

pa_tag = '<PA>'
pa_tag2 = '</PA>'
pb_tag = '<PB>'
pb_tag2 = '</PB>'

na_tag = '<NA>'
na_tag2 = '</NA>'
nb_tag = '<NA>'
nb_tag2 = '</NA>'

ea_tag = '<EA>'
ea_tag2 = '</EA>'
eb_tag = '<EB>'
eb_tag2 = '</EB>'

#태깅할 파일 제목 확장자 포함해서 입력
filename_for_tagging = '서울관광지.xlsx'

filename_for_saving = filename_for_tagging[:-5] + ' 태깅.txt'
saving = open(filename_for_saving, 'w')

filename_for_errlog = filename_for_tagging[:-5] + ' 에러로그.txt'
errlog = open(filename_for_errlog, 'w')

wb = xl.load_workbook('./' + filename_for_tagging)

for i in range(0, len(wb.sheetnames)):
    xlsx_sheet = wb[wb.sheetnames[i]]
    saving.write("[" + wb.sheetnames[i] + "]\n")

    df = pd.read_excel('./' + filename_for_tagging, sheet_name=wb.sheetnames[i])

    df['문장'] = df['문장'].str.strip().copy()
    df['문장'] = df['문장'].str.strip('\n').copy()

    df['수식관계/평점'] = df['수식관계/평점'].str.strip().copy()
    df['수식관계/평점'] = df['수식관계/평점'].str.strip('\n').copy()

    df['Unnamed: 6'] = df['Unnamed: 6'].str.strip().copy()
    df['Unnamed: 6'] = df['Unnamed: 6'].str.strip('\n').copy()

    df['Unnamed: 7'] = df['Unnamed: 7'].str.strip().copy()
    df['Unnamed: 7'] = df['Unnamed: 7'].str.strip('\n').copy()

    df['Unnamed: 8'] = df['Unnamed: 8'].str.strip().copy()
    df['Unnamed: 8'] = df['Unnamed: 8'].str.strip('\n').copy()

    df = df.fillna(pd.NA).copy()

    for j in range(1, df.shape[0] - 1):

        sent = df['문장'][j]
        n_str = df['수식관계/평점'][j]
        p_str = df['Unnamed: 6'][j]
        neg_str = df['Unnamed: 7'][j]
        emph_str = df['Unnamed: 8'][j]

        if n_str is not pd.NA:

            try:
                find = re.search(r'' + n_str.replace(' ', '*.'), str(sent)).span()
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

                    n_str = df['수식관계/평점'][check]
                    next_find = re.search(r'' + n_str.replace(' ', '*.'), str(sent)).span()
                    df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], f_tag + n_str + f_tag2)[j]
                    n_start = next_find[0]
                    sent = df['문장'][j]
                    
                    p_str = df['Unnamed: 6'][check]
                    next_find = re.search(r'' + p_str.replace(' ', '*.'), str(sent)).span()

                    if next_find[0] > n_start:
                        df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], pb_tag + p_str + pb_tag2)[j]
                        sent = df['문장'][j]
                    elif next_find[0] < n_start:
                        df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1], pa_tag + p_str + pa_tag2)[j]
                        sent = df['문장'][j]

                    sent = df['문장'][j]
                    
                    if check != df.shape[0] - 1:
                        check += 1
                
            except AttributeError:
                errlog.write(str(j) + "행 부근에서 에러 발생\n")
                
        elif n_str is pd.NA:
            continue

        if type(sent) is str:
            #xlsx_sheet['L' + str(j + 2)] = sent
            saving.write(str(j + 2) + "행 태깅: " + sent + "\n")
    

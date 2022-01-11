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

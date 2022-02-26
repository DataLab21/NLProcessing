import openpyxl as xl
import re
import pandas as pd

def clean_data(df):
    data = df.isnull()
    normal_data = df
    data_columns = df.columns
    print(data_columns)
    for d_c in data_columns:
        null_count = 0

        for i in range(len(data[d_c])):
            if(data[d_c][i]) == True:
                null_count += 1
        if null_count == len(data[d_c]):
            normal_data.drop([d_c],axis = 1, inplace = True)
    df1 = normal_data.loc[:,'문장']
    df2 = normal_data.loc[:,'수식관계/평점':]
    df3 = pd.concat([df1,df2],axis = 1)

    return df3

def tagging(num, df_list, str_list, tag_list, j, df, errlog):
    try:

        if df['문장'][j] is not pd.NA: df['문장'][j] = df['문장'][j].replace('$', '')

        find = re.search(r'' + str_list[1].replace(' ', '*.'), str(str_list[0])).span()

        if num == 1: df['문장'][j] = \
        df['문장'].str.slice_replace(find[0], find[1], tag_list[0][0] + str_list[1] + tag_list[0][1])[j]
        start = find[0]
        str_list[0] = df['문장'][j]

        find = re.search(r'' + str_list[num + 1].replace(' ', '*.'), str(str_list[0])).span()

        if find[0] > start:
            df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1],
                                                     "<" + tag_list[num][1] + ">" + str_list[num + 1][0] + "$" +
                                                     str_list[num + 1][1:] + "</" + tag_list[num][1] + ">")[j]
            str_list[0] = df['문장'][j]
        else:
            df['문장'][j] = df['문장'].str.slice_replace(find[0], find[1],
                                                     "<" + tag_list[num][0] + ">" + str_list[num + 1][0] + "$" +
                                                     str_list[num + 1][1:] + "</" + tag_list[num][0] + ">")[j]
            str_list[0] = df['문장'][j]

        check = j

        if check != df.shape[0] - 1:
            check = j + 1

        while df['문장'][check] is pd.NA:

            str_list[1] = df['수식관계/평점'][check]
            next_find = re.search(r'' + str_list[1].replace(' ', '*.'), str(str_list[0])).span()
            if num == 1: df['문장'][j] = \
            df['문장'].str.slice_replace(next_find[0], next_find[1], tag_list[0][0] + str_list[1] + tag_list[0][1])[j]
            start = next_find[0]
            str_list[0] = df['문장'][j]

            str_list[num + 1] = df[df_list[num + 1]][check]
            next_find = re.search(r'' + str_list[num + 1].replace(' ', '*.'), str(str_list[0])).span()
            if next_find[0] > start:
                df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1],
                                                         "<" + tag_list[num][1] + ">" + str_list[num + 1][0] + "$" +
                                                         str_list[num + 1][1:] + "</" + tag_list[num][1] + ">")[j]
                str_list[0] = df['문장'][j]
            else:
                df['문장'][j] = df['문장'].str.slice_replace(next_find[0], next_find[1],
                                                         "<" + tag_list[num][0] + ">" + str_list[num + 1][0] + "$" +
                                                         str_list[num + 1][1:] + "</" + tag_list[num][0] + ">")[j]
                str_list[0] = df['문장'][j]

            if check == df.shape[0] - 1:
                break
            else:
                check += 1

    except AttributeError:
        errlog.write(str(j + 2) + "행 부근에서 에러 발생 <" + str(num) + ">번째 테스트\n")

    # if num==3: print(str_list[0])

    if str_list[0] is not pd.NA: str_list[0] = str_list[0].replace('$', '')
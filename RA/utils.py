import numpy as np
import pandas as pd

def modifyQ(x):
    choice = pd.read_excel('data/choice.xlsx', sheet_name='Sheet1')
    caption = 99  # Default value
    for _, row in choice.iterrows():
        if row['ChoiceId'] == x:
            caption = row['ReportCaption']
            break
    return caption

def umodifyQ(x, q):
    choice = pd.read_excel('data/choice.xlsx', sheet_name='Sheet1')
    for _, row in choice.iterrows():
        if row['ReportCaption'] == x and row['QuestionId'] == q:
            return row['ChoiceId']
    return 999

def calass(a):
    if a < 300:
        return 1
    elif a < 460:
        return 2
    elif a < 570:
        return 3
    elif a < 680:
        return 4
    elif a < 790:
        return 5
    elif a < 900:
        return 6
    elif a <= 1000:
        return 7


def sortfunction(ba):
    sorted = np.zeros((1, 11))
    API_Service_Analysis=pd.read_excel('data/Service_Analysis.xlsx', sheet_name='Sheet1')
    for i in range(0,11):
        sorted[0,i]=99
        for index, row in API_Service_Analysis.iterrows():
            if row['ChoiceID']==ba[0,i]:
                sorted[0,i]=row['sortid']
    sorteddf = pd.DataFrame({'Q': [3, 4, 6, 7, 10, 11, 13, 17, 18, 19, 21]})
    sorteddf['sort']=sorted.reshape(-1, 1)
    sorteddf['score']=ba.reshape(-1, 1)
    df_sorted = sorteddf.sort_values(by='sort')
    return df_sorted

def filter_dic(d):
    filtered={key:value for key, value in d.items() if bool(value)}
    return filtered
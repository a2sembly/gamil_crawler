#-*- coding: utf-8 -*-
import csv
import os
import pandas as pd


def Save_to_CSV(data, path):
    # csv를 작성(추가)한다. fieldnames에 맞는 dictionary가 들어오면 필드에 맞게 csv를 쓴다.
    with open(path, 'a', newline="") as csvfile:
        fieldnames = ['Number', 'Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude','See-Level','MD5', 'SHA256']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)
    pass

def Make_to_CSV(path):
    # 초기 field(첫 번째 라인)을 구성하는 함수이다.
    with open(path, 'w',newline="") as csvfile:
        fieldnames = ['Number', 'Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude','See-Level','MD5', 'SHA256']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    pass

def CheckLastIndex(path): #내용추가될 경우 마지막라인 번호이후부터 추가하기 위해 lastinedex를 구하는 함수
    last_index = 0
    try:
        r = open(path,encoding='cp949')
        data = csv.reader(r)
        for rr in data:
            if rr[0] == 'Number':
                continue
            else:
                last_index = rr[0]
        r.close()
    except:
        return 0

    return last_index

def Read_to_CSV(path):
    r_data = []
    # csv파일을 읽는 함수
    with open(path, 'r') as csvfile:
        rdr = csv.reader(f)
        for line in rdf:
            r_data.append(line)
        f.close()
        return r_data
    pass
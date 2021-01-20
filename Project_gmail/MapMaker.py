#-*- coding: utf-8 -*-
from io import BytesIO
from PIL import Image
from urllib import request
import matplotlib.pyplot as plt
import SaveCSV
import requests
import json

gps = None

def Save_Map_Image(gps,path): # gps기반 맵 마킹
    try:
        api_key = "AIzaSyB2iKviLXaK-BKCXHw-giq807OWYYVuI1Y"
        url = "http://maps.googleapis.com/maps/api/staticmap?center=" + gps + "&size=800x800&zoom=14&markers=" + gps + "&sensor=false" + "&key=" + api_key

        buffer = BytesIO(request.urlopen(url).read())
        image = Image.open(buffer).convert('RGB')

        image.save(path)
    except:
        print(url)

def Save_Map_PolyGon(csv_path,image_path): # google static map
    locationArray = []
    api_key = "AIzaSyB2iKviLXaK-BKCXHw-giq807OWYYVuI1Y"
    # 모든 지도를 그리는 함수 전체 데이터가 저장된 csv를 읽고 지도를 그린다.
    data = SaveCSV.Read_to_CSV(csv_path)
    for idx, item in enumerate(data):
        if idx > 0 and item[5] != 'N/A' and item[6] != 'N/A':
            locationArray.append(item[5] + ',' + item[6])

    url = 'https://maps.googleapis.com/maps/api/staticmap?&zoom=1&size=640x640'
    for idx, loc in enumerate(locationArray):
        url = url + '&markers=color:red|label:' + str(idx + 1) + '|' + loc

    url = url + '&path=color:0x0000ff80|weight:5'

    # 경로를 설정한다.
    for idx, loc in enumerate(locationArray):
        url = url + '|' + loc

    # 이미지를 지정한 위치에 다운로드.
    url = url + '&key=' + api_key
    r = requests.get(url)
    print(url)
    header = r.headers['content-type'].split('/')
    if header[0] == "image":
        with open(image_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

    locationArray = []

def Check_See_Level(): # 해수면 값 조작 여부 검증
    api_key = "AIzaSyB2iKviLXaK-BKCXHw-giq807OWYYVuI1Y"
    url = 'https://maps.googleapis.com/maps/api/elevation/json?locations=' + gps + '&key='+api_key
    r = requests.get(url)
    js = json.loads(r.text)
    for item in js['results']:
        Altitude = item['elevation']
    
    return Altitude


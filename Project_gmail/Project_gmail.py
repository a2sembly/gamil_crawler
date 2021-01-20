#-*- coding: utf-8 -*-
from time import sleep
import time
import os
import re
import Downloader as down
import Selenium as sel
import Image_exif
import Hash
import SaveCSV as csv
import MapMaker as map
from urllib.parse import unquote
import Gamil as gm
import datetime

def main():
    # 헤더정보
    Data = {
        'Number': None,
        'Date': "",
        'Short URL': "",
        'Full URL': "",
        'Filename': "",
        'Latitude': "N/A",
        'Longitude': "N/A",
        'See-Level' :'N/A',
        'MD5': None,
        'SHA256': None
        }
         
    # CSV 파일 생성여부 검증
    if not os.path.isfile('Mail_data.csv'):
        csv.Make_to_CSV('Mail_data.csv')

    last_index_csv = int(csv.CheckLastIndex('Mail_data.csv')) # Number 설정을 위한 이전 CSV 데이터 확인

    # Gamil을 가져와서 파싱하는 코드
    M_data = gm.GetGmail()#sel.LoadUnReadMail("","")
    Mailtext = ""
    if len(M_data) != 0: # 읽어온 메일의 데이터가 존재한다면
        for i in range(len(M_data['Date'])): # 세부항목만큼 반복
                Data['Number'] = last_index_csv + 1 # csv index
                Data['Date'] = M_data['Date'][i] # 이메일 수신날짜
                date_cov = Data['Date'].split(' ') # 49번라인까지 이메일 날짜기반으로 폴더 생성
                d_name = date_cov[2] + "y" + " " + date_cov[1] + ", " + date_cov[3]
                d_name = datetime.datetime.strptime(d_name,'%B %d, %Y')
                d_name = d_name.strftime('%Y-%m-%d')
                dirname ="."+ d_name
                print(dirname)
                if not os.path.exists( dirname):
                    os.makedirs(dirname)
                Mailtext = M_data['Message'][i] # 본문 추출
                U_Data = down.Check_Correct_Url("https://bit.ly" + Mailtext) # URL에서 쓰레기값 검출
                Data['Short URL'] = U_Data[0]
                Data['Full URL'] = unquote(U_Data[1]) # URL 인코딩후 저장, 한글깨짐 방지
                Data['Filename'] = unquote(Data['Full URL'].split('/')[-1])
                Image_path = dirname + "/" + unquote(Data['Filename'])
                down.Download_image(Data['Full URL'],Image_path) # 이미지 다운로드

                G_Data = Image_exif.Image_Info(Image_path)
                if G_Data: # gps 데이터가 있는지 검증
                    Data['Latitude'] = G_Data['latitude']
                    Data['Longitude'] = G_Data['longitude']
                    map.Save_Map_Image(str(Data['Latitude']) + "," + str(Data['Longitude']),dirname + "/" + Data['Filename'] + "_MapImage.jpg")
                    map.gps = str(Data['Latitude']) + "," + str(Data['Longitude'])

                SL_Data = Image_exif.Image_Info_See_Level(Image_path)
                if SL_Data:
                    Data['See-Level'] = SL_Data['See-Level']

                H_Data = Hash.calc_file_hash(Image_path) # Hash 계산
                Data['MD5'] = H_Data['MD5']
                Data['SHA256'] = H_Data['sha256']

                print(Data)
                last_index_csv = last_index_csv + 1
                csv.Save_to_CSV(Data,'Mail_data.csv') # CSV 저장

    print('All data has been saved.')   

if __name__ == "__main__":
    main()
    map.Save_Map_PolyGon('Mail_data.csv','all_image.jpg')
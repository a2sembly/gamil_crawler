#-*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
import time
import re

def LoadUnReadMail(username, password):
    driver=webdriver.Chrome('chromedriver.exe')
    sleep(1)
    driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27') #스택오버플로우로 우회 로그인
    sleep(3)
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click() # Login With Google 버튼 클릭 
    driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="identifierNext"]').click() # id 입력
    sleep(3)
    driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click() # pw입력
    sleep(3)
    driver.get('https://gmail.com') # Gmail로 접속
    sleep(2)

    searchBox = driver.find_element_by_xpath('//*[@name="q"]') # 검색창
    searchBox.clear()
    searchBox.send_keys("is:unread from:(@@hotmail.com)" + "\n") # 읽지않은 메일로 필터 걸고 검색

    sleep(2)

    R_data = OpenMail(driver)
    return R_data

def OpenMail(driver):
    CheckM = False
    div_mailtext = ""
    div_mailtime = ""
    Short_Url = ""
    mailtime = ""
    while CheckM is False:
        try:
            driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[5]/div[2]/div/table/tbody').click() # 메일 리스트 확인 부분
            div_mailtext = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[3]/div[3]')
            div_mailtime = driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/span[2]')
            mailtime = time.strftime('%Y-%m-%d') + " " + div_mailtime.text.split('(')[0] # 시간 부분 파싱하고 년 월 일 형식으로 합쳐줌
            Short_Url = Find(div_mailtext.text)[0].replace('[','').replace(']','').replace('\'','') # 단축 url만듬

            CheckM = True
        except:
            searchBox = driver.find_element_by_xpath('//*[@name="q"]') # 검색창
            searchBox.clear()
            searchBox.send_keys("is:unread from:(@@@@@hotmail.com)" + "\n") # 읽지않은 메일로 필터 걸고 검색
            sleep(2)

    sleep(1)

    return [mailtime,Short_Url]

def Find(string): # - \n
  #정규표현식을 통하여 URL을 찾아내는 함수
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url]
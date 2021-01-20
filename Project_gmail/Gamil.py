#-*- coding: utf-8 -*-
import os
import email
import imaplib
import configparser
from time import sleep
import re
 
# 문자열의 인코딩 정보 추출 후, 문자열, 인코딩 얻기
def find_encoding_info(txt):
    info = email.header.decode_header(txt)
    s, encoding = info[0]
    return s, encoding
 
def GetGmail():
    # Email 설정정보 불러오기
    CheckM = False
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # gmail imap 세션 생성
    session = imaplib.IMAP4_SSL('imap.gmail.com')
    
    # 로그인
    session.login(config['Gmail']['ID'], config['Gmail']['PW'])
    
    # 받은편지함
    session.select('Inbox')
    
    # 받은 편지함 내 모든 메일 검색
    result, data = session.uid('search', None, 'UNSEEN (HEADER From "@@@hotmail.com")') 
    
    # 여러 메일 읽기
    all_email = data[0].split()
    print(len(all_email))
    Date = []
    Message = []
    while CheckM is False:
        if len(all_email) == 0:
            result, data = session.uid('search', None, 'UNSEEN (HEADER From "@@hotmail.com")')
            all_email = data[0].split()
        else:
            for mail in all_email:
                result, data = session.uid('fetch', mail, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                
                # 메일 정보
                Date.append(email_message['Date'])
                message = ''
                #메일 본문 확인
                if email_message.is_multipart():
                    for part in email_message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            bytes = part.get_payload(decode=True)
                            encode = part.get_content_charset()
                            message = message + str(bytes, encode)
                else:
                    if email_message.get_content_type() == 'text/plain':
                        bytes = email_message.get_payload(decode=True)
                        encode = email_message.get_content_charset()
                        message = str(bytes, encode)
                Message.append(Find(message))
            CheckM = True

    session.close()
    session.logout()
    return {'Date': Date,'Message':Message}

def Find(string): # - \n
  #정규표현식을 통하여 URL을 찾아내는 함수
    url = re.compile(r"[^((http(s?))\:\/\/)]([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?", re.MULTILINE|re.UNICODE)
    urls = re.findall(url, string)
    return urls[0][2]
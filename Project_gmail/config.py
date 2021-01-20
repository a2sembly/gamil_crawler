#-*- coding: utf-8 -*-
import configparser
 
# ConfigParser 객체 생성
config = configparser.ConfigParser()
 
# 세션 생성
config['Gmail'] = {}
 
# option, value 생성 방법 1
config['Gmail']['ID'] = ''
config['Gmail']['PW'] = ''
 
# config.ini 파일 생성
with open('config.ini', 'wt', encoding='UTF-8') as conf_file:
    config.write(conf_file)
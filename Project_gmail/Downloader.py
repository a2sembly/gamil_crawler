#-*- coding: utf-8 -*-
import requests
# requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def Download_image(url,path):
    try:
        r = requests.get(url, stream=True, verify=False)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        return True

    except:
        return False

def Check_Correct_Url(url):
        # 메일내 URL에 대한 쓰레기값 검증 함수
        Correct_URL = ""

        # d_data가 False가 아닐 때 까지 무한 반복한다.
        while True:
            r = requests.get(url, stream=True, verify=False)
            if r.status_code == 200 and r.headers['content-type'].split('/')[0] == "image": 
                # 웹 서버와 정상연결되었고, content-tpye이 image일 경우
                Correct_URL = r.url
                break
            else:
                url = url[0:-1] # image가 아닐경우 뒤에서 한글자를 삭제한 후 다시 반복, 쓰레기값 검출용

        return [url,Correct_URL]
import requests
from bs4 import BeautifulSoup #정적 페이지 크롤링을 위한 모듈
import base64 #링크 해독
from urllib.parse import quote, unquote #링크해독 2
from datetime import datetime, timedelta, date #시간 계산, 요일 확인
import time #현재 시간 불러오기
from fake_useragent import UserAgent #useragent 모듈

#universityMeal_Url_origin = "fnct1|@@|/diet/kr/2/view.do?monday=2025.06.30&week=next&" 

"""
today = date.today() #오늘의 날짜 불러오기
next_day = today + timedelta(days=7) #7일 후 날짜 계산
formatted_day = next_day.strftime("%Y.%m.%d") #2025.07.04 형태로 출력


before_link_str = "fnct1|@@|/diet/kr/2/view.do?monday="+formatted_day+"&week=next&"
before_link_bytes = before_link_str.encode('UTF-8') #문자열 url을 byte형태로 바꾸기
## encoded_data = quote(before_link_bytes, safe='') #퍼센트 인코딩 
## result_link = base64.b64encode(encoded_data) #base64 인코딩
result_link = base64.b64encode(before_link_bytes) #base64 인코딩
encoded_data = quote(result_link, safe='') #퍼센트 인코딩 


data = [] #db에 넣기전 리스트 선언
url = "https://www.inha.ac.kr/kr/1072/subview.do?&enc=" + encoded_data #최종 주소 결합
"""

user_agent = UserAgent()
headers = {'User-Agent': user_agent.random} #user agent 설정


response = requests.get("https://www.inha.ac.kr/kr/1072/subview.do?&enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtyJTJGMiUyRnZpZXcuZG8lM0Ztb25kYXklM0QyMDI1LjA2LjIzJTI2d2VlayUzRHByZSUyNg==", headers=headers) 
html = response.text


soup = BeautifulSoup(html, 'html.parser')

# 1. 모든 요일 제목(h2)을 찾는다.
day_headings = soup.select('#viewForm > div:nth-child(5) > div > div > table > tbody > tr:nth-child(1) > td.left')



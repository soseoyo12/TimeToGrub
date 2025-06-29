import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json # 결과를 보기 좋게 출력하기 위해 import

# 1. 크롤링 대상 URL 설정 및 요청
user_agent = UserAgent()
headers = {'User-Agent': user_agent.random}
url = "https://www.inha.ac.kr/kr/1073/subview.do?&enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtyJTJGMSUyRnZpZXcuZG8lM0Ztb25kYXklM0QyMDI1LjA2LjIzJTI2d2VlayUzRG5leHQlMjY="
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # HTTP 요청 실패 시 에러 발생
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 2. 날짜별로 묶인 div 컨테이너를 모두 선택
    daily_boxes = soup.select('div.food_list_box')

    if not daily_boxes:
        print("식단 정보를 담고 있는 'div.food_list_box'를 찾을 수 없습니다. 페이지 구조를 확인하세요.")

    weekly_menu_data = [] # 일주일치 식단을 저장할 리스트

    # 3. 각 날짜별 div를 순회하며 데이터 추출
    for box in daily_boxes:
        # 3-1. 날짜 제목(h4) 추출
        date_h4 = box.select_one('h4')
        date_str = date_h4.text.strip() if date_h4 else "날짜 정보 없음"
        
        daily_menu = {
            'date': date_str,
            'corners': {}
        }

        # 3-2. 코너별 메뉴(li) 목록을 모두 선택
        corner_list = box.select('ul > li')

        for corner_li in corner_list:
            # 3-3. 코너명(strong)과 메뉴 내용(p)을 각각 추출
            corner_name_strong = corner_li.select_one('strong')
            menu_p = corner_li.select_one('p')

            if corner_name_strong and menu_p:
                corner_name = corner_name_strong.text.strip()
                menus_text = menu_p.text.strip()
                
                # 3-4. 메뉴 텍스트를 쉼표(,) 기준으로 분리하고 공백 제거
                menu_items = [menu.strip() for menu in menus_text.split(',') if menu.strip()]
                
                daily_menu['corners'][corner_name] = menu_items

        weekly_menu_data.append(daily_menu)

    # 4. 최종 결과 출력 (JSON 형태로 보기 좋게 출력)
    # 나중에 API 서버를 만들 때 이런 형태로 데이터를 보내주면 됩니다.
    print(json.dumps(weekly_menu_data, indent=2, ensure_ascii=False))


except requests.exceptions.RequestException as e:
    print(f"HTTP 요청 중 에러가 발생했습니다: {e}")
except Exception as e:
    print(f"알 수 없는 에러가 발생했습니다: {e}")
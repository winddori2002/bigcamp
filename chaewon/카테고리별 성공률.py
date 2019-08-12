import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains

# 크롬드라이버 실행 및 로그인
driver = webdriver.Chrome('./chromedriver')

# 전체 프로젝트 목록 페이지로 가기(종료된 프로젝트들 마감임박순으로 나열한 페이지)
base_link = 'https://www.wadiz.kr/web/wreward/category/310?keyword=&endYn=Y&order=closing'
driver.get(base_link)

time.sleep(1)

# 맨 아래로 스크롤하기
SCROLL_PAUSE_TIME = 1
while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue

time.sleep(10)

# 개별 프로젝트 컨테이너 찾기
projects = driver.find_elements_by_css_selector('div.ProjectCardList_item__1owJa')

success = 0
fail = 0

for p in projects:
    percent = p.find_element_by_css_selector('span.RewardProjectCard_percent__edRT9').text.replace('%', '')
    if int(percent) < 100:
        fail += 1
    else:
        success += 1

print('전체 갯수:', len(projects))
print('성공률:', success/len(projects)*100)
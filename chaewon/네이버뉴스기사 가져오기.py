import requests
from bs4 import BeautifulSoup
import openpyxl
import re
from selenium import webdriver
import time

# 엑셀 파일 만들기
wb = openpyxl.Workbook()
sheet = wb.active

sheet.append(['키워드', '기사제목', '날짜'])

# 검색할 키워드
keyword = input("검색하실 키워드는?:")

# 크롬 드라이버
driver = webdriver.Chrome('./chromedriver')

# 가져올 기사의 개수 명시
max = 20

def check_exists_by_css_selector(css_selector):
    try:
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True

for n in range(1, max, 10):
    driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + keyword + "&start=" + str(n))

    articles = driver.find_elements_by_css_selector('ul.type01>li')

    for a in articles:
        # 기사 제목 가져오기
        title = a.find_element_by_css_selector("a._sp_each_title").text
        # 기사 날짜 가져오기
        date = a.find_element_by_css_selector("dd.txt_inline").text

        print(title)

        # 연관 기사 가져오기
        if check_exists_by_css_selector('ul.type01>li dl dd:nth-of-type(3)') == True:
            try:
                more_button = a.find_element_by_css_selector('ul.type01>li div.newr_more a')
                more_button.click()

                time.sleep(2)

                more_articles = driver.find_elements_by_css_selector('ul.type01>li')

                for m in more_articles:
                    # 기사 제목 가져오기
                    more_title = m.find_element_by_css_selector("a._sp_each_title").text
                    # 기사 날짜 가져오기
                    more_date = m.find_element_by_css_selector("dd.txt_inline").text

                    print(more_title)
                    sheet.append([keyword, more_date, more_title])

            except:
                related_articles = a.find_elements_by_css_selector('ul.type01>li ul.relation_lst li')
                for r in related_articles:
                    related_articles_title = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li a').text
                    related_articles_date = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li span.txt_sinfo').text

                    print(related_articles_title)
                    sheet.append([keyword, related_articles_date, related_articles_title])

        sheet.append([keyword, date, title])

wb.save("네이버뉴스키워드.xlsx")
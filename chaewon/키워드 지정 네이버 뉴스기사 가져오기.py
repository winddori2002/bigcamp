import requests
from bs4 import BeautifulSoup
import openpyxl
import re
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# 엑셀 파일 만들기
wb = openpyxl.Workbook()
sheet = wb.active

sheet.append(['키워드', '날짜', '기사제목'])

# 검색할 키워드
keyword = '크라우드펀딩'

# 크롬 드라이버(창 띄우기 않고 데이터 가져오게 설정)
options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome('./chromedriver', options=options)

# 가져올 기사의 개수 명시
max = 3999

def check_exists_by_css_selector(css_selector):
    try:
        driver.find_element_by_css_selector(css_selector)
    except:
        return False
    return True

for n in range(1, max, 10):
    driver.get('https://search.naver.com/search.naver?&where=news&query=크라우드펀딩&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds=2019.06.01&de=2019.08.14&docid=&nso=so:dd,p:from20190601to20190814,a:all&mynews=0&start='+str(n)+'&refresh_start=0')
    articles = driver.find_elements_by_css_selector('ul.type01>li')

    for a in articles:
        # 기사 제목 가져오기
        title = a.find_element_by_css_selector("a._sp_each_title").text
        # 기사 날짜 가져오기
        date = a.find_element_by_css_selector("dd.txt_inline").text

        print(title)
        sheet.append([keyword, date, title])

        # 연관 기사 가져오기
        if check_exists_by_css_selector('ul.type01>li dl dd:nth-of-type(3)') == True:
            # 연관 기사가 많아 더보기 버튼이 있을 경우
            try:
                more_button = a.find_element_by_css_selector('ul.type01>li div.newr_more').text
                num_of_more_articles = re.search(r'(\d+)', more_button)
                for _ in range(int(num_of_more_articles.group(1))):
                    sheet.append([keyword, date, '[연관기사]'+title])
                    print('연관기사')

            # 연관 기사가 몇 개 없는 경우
            except:
                related_articles = a.find_elements_by_css_selector('ul.type01>li ul.relation_lst li')
                for r in related_articles:
                    related_articles_title = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li a').text
                    related_articles_date = r.find_element_by_css_selector('ul.type01>li ul.relation_lst li span.txt_sinfo').text

                    print(related_articles_title)
                    sheet.append([keyword, related_articles_date, related_articles_title])

print('수집 완료')

wb.save("네이버뉴스키워드.xlsx")
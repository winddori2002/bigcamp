import requests
from bs4 import BeautifulSoup
import openpyxl

wb = openpyxl.load_workbook("네이버뉴스.xlsx")
sheet = wb.active

max = 100
keyword = input("검색하실 키워드는?:")

for n in range(1, max, 10):
    raw = requests.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + keyword + "&start=" + str(n),
                       headers={'User-Agent':'Mozilla/5.0'})

    html = BeautifulSoup(raw.text, "html.parser")

    articles = html.select("ul.type01>li")

    for a in articles:
        title = a.select_one("a._sp_each_title").text
        source = a.select_one("span._sp_each_source").text
        search = keyword

        print(title, source)
        sheet.append([keyword, title, source])

wb.save("네이버뉴스.xlsx")

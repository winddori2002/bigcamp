import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import openpyxl
from selenium.webdriver.common.action_chains import ActionChains

# 엑셀 파일 만들기
wb = openpyxl.Workbook()
sheet = wb.active

# 맨 윗줄에 컬럼명 추가
sheet.append(['url', '제목', '카테고리', '메이커', '달성률', '달성액', '서포터수', '좋아요수', '요약글', '목표금액과기간', '글업데이트수', '댓글수', \
              '리워드종류수', '이미지수', '비디오수', '배송시작날짜', '인스타팔로워수', '와디즈팔로워수', '과거프로젝트수', '과거성공프로젝트수'])

# 크롬드라이버 실행 및 로그인
driver = webdriver.Chrome('./chromedriver')

# 내 계정으로 로그인하기
login_link = 'https://www.wadiz.kr/web/waccount/wAccountLogin?returnUrl=https://www.wadiz.kr/web/main'
driver.get(login_link)
id = driver.find_element_by_css_selector('input#userName')
id.send_keys('') # 본인 이메일 쓸 것
pw = driver.find_element_by_css_selector('input#password')
pw.send_keys('') # 본인 비번 쓸 것
login_btn = driver.find_element_by_css_selector('button#btnLogin')
login_btn.click()

time.sleep(1.5)

# 전체 프로젝트 목록 페이지로 가기(종료된 프로젝트들 마감임박순으로 나열한 페이지)
base_link = 'https://www.wadiz.kr/web/wreward/category/308?keyword=&endYn=Y&order=closing'
driver.get(base_link)
driver.maximize_window()

time.sleep(1)


# 맨 아래로 스크롤하기
while True:
    try:
        target = driver.find_element_by_css_selector('button.ProjectListMoreButton_button__27eTb')
        actions = ActionChains(driver)
        actions.move_to_element(target)
        actions.perform()
        time.sleep(2)
    except:
        break


# 개별 프로젝트 컨테이너 찾기
projects = driver.find_elements_by_css_selector('div.ProjectCardList_item__1owJa')

count = 1
idx = 0

for p in projects:

    print(count)
    # 전체 목록에서 정보 가져오기

    image = p.find_element_by_css_selector('a.ProjectCardLink_link__2X36I.CommonProjectCard_image__1aEog')

    try:
        name = p.find_element_by_css_selector('p.CommonProjectCard_title__28lHZ.RewardProjectCard_title__RDEBu').text
    except:
        name = 'no info'

    try:
        category = p.find_element_by_css_selector('span.RewardProjectCard_category__1vo_V').text
    except:
        category = 'no info'

    try:
        maker = p.find_element_by_css_selector('span.RewardProjectCard_makerName__2sITk').text
    except:
        maker = 'no info'

    try:
        percent = p.find_element_by_css_selector('span.RewardProjectCard_percent__edRT9').text.replace('%', '')
    except:
        percent = 'no info'

    try:
        money = p.find_element_by_css_selector('span.RewardProjectCard_amount__2GV5X').text.replace(',', '')
    except:
        money = 'no info'

    print(name)


    # 새로운 브라우저 탭에서 프로젝트 세부 페이지 들어가기
    project_url = image.get_attribute('href')

    driver.execute_script("window.open('');")
    time.sleep(1.5)


    # 크롬 드라이버의 포커스를 새로운 탭(세부 페이지)으로 옮기기
    driver.switch_to.window(driver.window_handles[1])
    driver.get(project_url)
    time.sleep(1.5)

    # 서포터 수
    try:
        supporters = driver.find_element_by_css_selector('p.total-supporter strong').text
    except:
        supporters = 0

    # 좋아요(하트) 수
    try:
        likes = driver.find_element_by_css_selector('em.cnt-like').text
    except:
        likes = 0

    # 요약글 텍스트
    try:
        summary = driver.find_element_by_css_selector('div.campaign-summary').text
    except:
        summary = 'None'

    # 프로젝트 목표 금액과 기간
    try:
        goal_amount = driver.find_element_by_css_selector('div.wd-ui-campaign-content > div > div:nth-child(4) p').text
    except:
        goal_amount = 'no info'

    # 새로운 글 업데이트 수
    try:
        new_news = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(4) span').text
    except:
        new_news = 0

    # 댓글 수(커뮤니티 수)
    try:
        comment_num = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(5) span').text
    except:
        comment_num = 0

    # 리워드 종류 수
    try:
        reward_num = len(driver.find_elements_by_css_selector('button.rightinfo-reward-list'))
    except:
        reward_num = 0

    # 소개글 이미지 수
    try:
        img_num = len(driver.find_elements_by_css_selector('div.inner-contents.fr-view img'))
    except:
        img_num = 0

    # 소개글 비디오 수
    try:
        video_num = len(driver.find_elements_by_css_selector('span.fr-video.fr-fvc.fr-dvb.fr-draggable'))
        print(video_num)
    except:
        video_num = 0
        print(video_num)



    # 펀딩 안내 페이지 들어가기
    funding_info_btn = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(3) a')
    funding_info_btn.click()

    # 배송 시작 날짜
    try:
        delivery_date = driver.find_element_by_css_selector('div#detail-funding-info div.content h3 em').text
    except:
        deliver_date = 'no info'

    # 커뮤니티 페이지 들어가기
    community_btn = driver.find_element_by_css_selector('ul.tab-list li:nth-of-type(5) a')
    community_btn.click()

    # 댓글(굳이 필요?)

    # 새로운 탭에서 인스타그램 열어 팔로워 수 가져오기
    try:
        instagram = driver.find_element_by_css_selector('ul.social a.instagram')
        instagram_url = instagram.get_attribute('href')

        driver.execute_script("window.open('');")
        time.sleep(1.5)

        driver.switch_to.window(driver.window_handles[2])
        driver.get(instagram_url)
        time.sleep(1.5)
        try:
            # 인스타 팔로워 수
            sns_followers = driver.find_element_by_css_selector('ul.k9GMp  li:nth-of-type(2)  span.g47SY').text
        except:
            # 링크에 에러가 있거나 계정이 삭제된 경우
            sns_followers = 'link error'

        driver.close()
        time.sleep(1.5)

        driver.switch_to.window(driver.window_handles[1])
    except:
        sns_followers = 'no account'

    time.sleep(1.5)


    # 새로운 탭에서 메이커 프로필 페이지 가기
    maker_profile = driver.find_element_by_css_selector('div.maker-info button')
    maker_profile.click()

    time.sleep(1.5)

    # 와디즈 팔로워 수
    try:
        wadiz_followers = driver.find_element_by_css_selector('ul.activity-list li:nth-of-type(3) strong').text
    except:
        wadiz_followers = 0

    # 과거 리워드 프로젝트 수
    try:
        past_projects_num = len(driver.find_elements_by_css_selector('li.all em.project-type.reward'))-1
    except:
        past_projects_num = 0

    # 과거 성공한 프로젝트 수(현재 포함)
    try:
        past_projects = driver.find_elements_by_css_selector('li.all span.percent')
        n = 0
        for past in past_projects:
            if int(past.text.replace('%', '')) >= 100:
                n += 1
        past_success_projects_num = n
    except:
        past_success_projects_num = 0


    # 엑셀 시트에 데이터 쓰기
    sheet.append([project_url, name, category, maker, percent, money, supporters, likes, summary, goal_amount, new_news, comment_num,\
                  reward_num, img_num, video_num, delivery_date, sns_followers, wadiz_followers, past_projects_num, \
                  past_success_projects_num])


    # 세부 페이지 탭 닫기
    driver.close()
    time.sleep(1.5)

    # 원래 탭(전체 목록 페이지)로 돌아가기
    driver.switch_to.window(driver.window_handles[0])
    
    count += 1

    fileName = 'Wadiz1{index}{ext}'.format(index=idx, ext='.xlsx')
    wb.save(fileName)
    idx += 1

# 크롬드라이버 닫기
driver.close()

print('수집 종료')

# 엑셀 파일 저장하기
wb.save('Wadiz.xlsx')

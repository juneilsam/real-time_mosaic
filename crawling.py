import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
from urllib.request import urlretrieve, build_opener, install_opener
from urllib.error import HTTPError, URLError
from tqdm import tqdm
from PIL import Image

def web_crawler(keyword):
    print("[크롤링 시작]")
    # 폴더 생성
    print("[경로 확인]")
    dir_name = 'C:/Users/yreis/Study/project/dataset/{}'.format(keyword)

    if not os.path.isdir(dir_name):
            os.mkdir(dir_name)


    # 웹 접속 - 구글 이미지 접속
    print("[검색 시작]")
    driver = webdriver.Chrome('C:/Users/yreis/Study/chromedriver.exe')
    driver.get('https://google.com')

    input_box = driver.find_element_by_css_selector('#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input')
    input_box.send_keys("smiling")
    input_box.send_keys(Keys.RETURN)
    link = driver.find_element_by_css_selector("#hdtb-msb-vis > div:nth-child(2) > a")
    link.click()

    # 스크롤 다운
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    SCROLL_COUNT = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    after_click = False

    print("[스크롤 다운 시작]\n[스크롤 진행 상황]")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        SCROLL_COUNT += 1
        print(str(SCROLL_COUNT) + "페이지")
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height

    print("[스크롤 종료]")
    print("[검색 종료]")


    # 이미지 저장
    print("[이미지 저장 시작]")
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    
    count = 1
    
    for image in tqdm(images):
        try:
            image.click()
            time.sleep(2)
            imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
            extension = imgUrl.split(".")[-1]
            opener = build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            install_opener(opener)
            if extension in ["jpg", "jpeg", "png", "bmp"]:
                urlretrieve(imgUrl, dir_name + '/' + str(count) + "." + extension)
                count += 1
            else:
                pass
                
            """
            # 테스트 시 갯수 제한
            if count == 21:
                break                
            """
            
        except:
            pass

    print("[이미지 저장 종료]")


    # 이미지 필터
    print("[이미지 필터링 시작]")
    filtered_count = 0
    filter_size = 400

    for file_name in os.listdir(dir_name):
        try:
            file_path = os.path.join(dir_name, file_name)
            print(file_path)
            im = Image.open(file_path)

            if im.width < filter_size and im.height < filter_size:
                im.close()
                os.remove(file_path)
                print(f"이미지 {file_name} 제거")
                filtered_count += 1
        except OSError as e:
            os.remove(file_path)
            filtered_count += 1
    print("[총" +" "+ str(filtered_count) +"개 이미지 삭제]" )

    print("[이미지 필터링 종료]")

    driver.close()

    print("[크롤링 종료]")


#검색 대상 설정
keyword_list = ["smiling", "laugh"]

for keyword in keyword_list:
    web_crawler(keyword)

import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve, build_opener, install_opener

from tqdm import tqdm
from PIL import Image

# 상대경로를 설정하기 위한 함수 (https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 크롤링 함수
def web_crawler(keyword):
    print("[크롤링 시작]")

    print("[경로 확인]")

    # 폴더가 없을 경우 생성후 경로 지정
    try:
        # 디렉토리가 이미 존재할 경우 에러가 발생하기 때문에 except로 넘어간다.
        os.makedirs(resource_path(f'downloads\{keyword}'))
        # 경로 설정
        dir_name = resource_path(f'downloads\{keyword}')

    # 폴더가 있는 경우(에러가 발생하지 않는 경우) 경로 설정
    except:
        dir_name = resource_path(f'downloads\{keyword}')

    # 웹 접속 - 구글 이미지 접속
    print("[검색 시작]")

    # 크롬드라이버 옵션
    options = webdriver.ChromeOptions()
    # 로그 숨기기
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 백그라운드에서 실행되게 함
    options.add_argument("headless")
    # 크롬드라이버 경로 지정
    driver = webdriver.Chrome(resource_path('chromedriver.exe'), options=options)
    # 접속할 주소 설정
    driver.get('https://google.com')

    # 입력창의 경로를 selector 경로로 지정
    input_box = driver.find_element_by_css_selector(
        'body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input')
    # 검색할 키워드 입력
    input_box.send_keys(keyword)
    # 검색 실행
    input_box.send_keys(Keys.RETURN)
    # '이미지' 버튼을 찾아서 클릭
    link = driver.find_element_by_css_selector("#hdtb-msb > div:nth-child(1) > div > div:nth-child(2) > a")
    link.click()

    # 스크롤 다운
    SCROLL_PAUSE_TIME = 1
    # 스크롤 횟수 카운트
    SCROLL_COUNT = 0
    # 이전 스크롤의 높이
    last_height = driver.execute_script("return document.body.scrollHeight")
    after_click = False

    print("[스크롤 다운 시작]\n[스크롤 진행 상황]")

    while True:
        # 0부터 해당 맨 아래(페이지의 높이만큼)까지 스크롤링
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 페이지 로딩
        time.sleep(SCROLL_PAUSE_TIME)
        # 스크롤링 횟수 증가
        SCROLL_COUNT += 1
        print(str(SCROLL_COUNT) + "페이지")
        # 새 스크롤 높이(맨 아래 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        # 새 높이와 지난 높이가 같은 경우
        if new_height == last_height:
            # 더 보기 버튼 클릭
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            # 버튼을 클릭할 수 없는 경우 정지
            except:
                break
        # 이전 스크롤의 높이를 업데이트 해줌
        last_height = new_height

    print("[스크롤 종료]")
    print("[검색 종료]")

    # 이미지 저장
    print("[이미지 저장 시작]")
    # 각 이미지들의 경로를 설정
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

    count = 1

    # 이미지 저장 시작
    for image in tqdm(images):
        try:
            image.click()
            time.sleep(2)
            # 사진 url 추출
            imgUrl = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img').get_attribute(
                "src")

            # 확장자 추출
            extension = imgUrl.split(".")[-1]

            # 자동화 프로그램의 접근이 어려운 사이트의 접속을 위함
            opener = build_opener()
            # 헤더설정
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            install_opener(opener)

            # 확장자를 설정하고 해당 확장자의 사진 파일명, 경로를 설정
            if extension in ["jpg", "jpeg", "png", "bmp"]:
                urlretrieve(imgUrl, dir_name + '/' + str(count) + "." + extension)
                # 파일명 설정을 위함
                count += 1
            else:
                pass

            """
            # 테스트 시 갯수 제한
            if count >= 21:
                break                
            """
        # 예외처리
        except:
            pass

    print("[이미지 저장 종료]")

    """
    # 이미지 필터
    print("[이미지 필터링 시작]")
    filtered_count = 0

    # 이미지 크기 설정
    filter_size = 400

    # 파일이 저장된 곳에서 이미지 필터링을 수행
    # 저장 경로에서 이미지 리스트 추출
    for file_name in os.listdir(dir_name):
        try:
            # 파일의 경로를 설정
            file_path = os.path.join(dir_name, file_name)
            print(file_path)
            # 이미지 오픈
            im = Image.open(file_path)
            
            # 이미지의 가로세로 길이와 필터 사이즈를 비교
            if im.width < filter_size and im.height < filter_size:
                # 이미지 파일 닫기
                im.close()
                # 이미지 파일 제거
                os.remove(file_path)
                print(f"이미지 {file_name} 제거")
                filtered_count += 1
        # 예외처리        
        except OSError as e:
            os.remove(file_path)
            filtered_count += 1

    print("[총" + " " + str(filtered_count) + "개 이미지 삭제]")

    print("[이미지 필터링 종료]")
    """
    
    # 드라이버 종료
    driver.close()

    print("[크롤링 종료]")


# 검색 대상 설정
keyword_list = ["laugh"]

# 모든 키워드들에 대해 함수 적용
for keyword in keyword_list:
    web_crawler(keyword)

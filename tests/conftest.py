import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    chrome_option = Options()

    #chrome_option.add_argument("--headless")                # Jenkins용
    chrome_option.add_argument("--disable-extensions")      # 크롬 확장 프로그램 비활성화
    chrome_option.add_argument("--disable-popup-blocking")  # 팝업 차단 해제
    chrome_option.add_argument("--disable-gpu")             # GPU사용 X, CPU만 사용 가벼운 테스트 진행
    chrome_option.add_argument("--no-sandbox")              # 샌드박스 보안 기능 종료, 실행 속도 향상 (리눅스 권한 문제 피할때도 사용)
    chrome_option.add_argument("--disable-dev-shm-usage")   # 메모리 부족 방지 (공유 메모리 디렉토리 미사용)
    chrome_option.add_argument("--log_level=3")             # 콘솔 로그 레벨 낮춤, 에러나 중요한 정보만 출력
    chrome_option.add_argument("--window-size=1920,1080")   # 브라우저 창크기 고정 (해상도에 따라 위치가 바뀌는 것 방지)
    chrome_option.page_load_strategy = "eager"              # 기본값은 normal → eager: HTML 요소만 로딩되면 바로 테스트

    driver = webdriver.Chrome(service=Service(), options=chrome_option)

    yield driver

    driver.quit()

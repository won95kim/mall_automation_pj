import os, logging, time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoAlertPresentException

''' 로그, 스크린샷 설정 '''
def utils_reports_set(page_name, func_name):
    LOG_DIR = f"reports/logs/{page_name}"
    SCREENSHOT_DIR = f"reports/screenshots/{page_name}"

    # 폴더 없을 시 생성, 기존에 존재할 경우 에러 없이 넘어감
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # 로그 설정
    logger = logging.getLogger()

    # 로그 중복을 막기 위한 핸들러 초기화
    logger.handlers.clear()

    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(f"{LOG_DIR}/{page_name}.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"))
    logger.addHandler(file_handler)

    # 스크린샷 설정
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    screenshot = os.path.join(SCREENSHOT_DIR, f"{timestamp}_{func_name}.jpg")

    return logger, screenshot


''' 알럿 처리 '''
def utils_alert(driver: WebDriver):
    while True:
        try:
            alert = driver.switch_to.alert  # 장바구니에 상품이 있을 시 알럿 발생 시, 확인 버튼 클릭
            alert_text = alert.text
            alert.accept()
        except NoAlertPresentException:
            break    # 장바구니에 상품이 없을 시, 알럿 발생하지 않음
    return alert_text
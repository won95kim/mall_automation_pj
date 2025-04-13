import pytest
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv

from src.utils import utils_reports_set
from src.recent_page import RecentPage

load_dotenv()   # env 파일 로드

# 테스트 데이터 상수 정의
GOODS_URL = os.getenv("GOODS_URL")
TODAY_GOODS_URL = os.getenv("TODAY_GOODS_URL")
BRAND_ID = "70015"
PAGE_NAME = "test_recent_page"

@pytest.mark.usefixtures("driver")
class TestDetailPage:

    ''' 오늘 본 상품 정보 확인 테스트 '''
    def test_compare_today_goods_info(slef, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        recent_page = RecentPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품상세 페이지 진입
            driver.get(GOODS_URL)

            # 상품상세 페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품상세 페이지 진입 확인")

            # 상품 정보 저장
            goods_list = recent_page.save_goods_info()

            # 오늘 본 상품 페이지 진입
            driver.get(TODAY_GOODS_URL)

            # 오늘 본 상품 페이지 진입 확인
            wait.until(EC.url_contains("todaygoods"))
            assert "todaygoods" in driver.current_url
            logger.info("오늘 본 상품 페이지 진입 확인")

            # 오늘 본 상품 정보 저장
            today_goods_list = recent_page.save_today_goods_info()

            # 오늘 본 상품 저장 확인 (방금 본 상품과 동일한지 확인)
            assert goods_list == today_goods_list # 이름, 가격이 전부 동일하면 PASS
            logger.info("오늘 본 상품 저장 확인")

        except NoSuchElementException:
            logger.warning("요소를 찾을 수 없습니다. NoSuchElementException")
            driver.save_screenshot(screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            driver.save_screenshot(screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            driver.save_screenshot(screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)

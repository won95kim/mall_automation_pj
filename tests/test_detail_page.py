import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from src.utils import utils_reports_set, utils_alert
from src.detail_page import DetailPage

# 테스트 데이터 상수 정의
URL = "https://www.nibbuns.co.kr/shop/shopdetail.html?branduid=70015"
BRAND_ID = "70015"
OPTIONS = ["아이보리"]
GOODS_TAB_OPTIONS = ["detailGoodsInfo", "detailReview", "detailQna", "detailRelation", "detailChange"]
PAGE_NAME = "test_detail_page"

@pytest.mark.usefixtures("driver")
class TestDetailPage:

    ''' [단위] 상품 옵션 클릭 테스트 '''
    @pytest.mark.parametrize("option_index", [0])   # 상품의 옵션 수에 따라 변경
    def test_select_option(self, driver: WebDriver, request, option_index):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품 상세페이지 진입
            driver.get(URL)

            # 상품 상세페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품 상세페이지 진입 확인")

            # 상품 옵션 클릭
            detail_page.select_option(OPTIONS[option_index])

            # 상품 옵션 클릭 확인
            goods_list = detail_page.save_goods_info()  # 현재 상품 정보 저장(이름, 옵션, 가격)
            assert OPTIONS[option_index] in goods_list[1]
            logger.info("상품 옵션 클릭 확인")

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
    

    ''' [단위] 바로 구매 버튼 클릭 테스트 (비로그인 기준) '''
    def test_buy_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품 상세페이지 진입
            driver.get(URL)

            # 상품 상세페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품 상세페이지 진입 확인")

            # 상품 옵션 클릭
            detail_page.select_option(OPTIONS[0])

            # 상품 옵션 클릭 확인
            goods_list = detail_page.save_goods_info()  # 현재 상품 정보 저장(이름, 옵션, 가격)
            assert OPTIONS[0] in goods_list[1]
            logger.info("상품 옵션 클릭 확인")

            # 바로 구매 버튼 클릭
            detail_page.buy_btn_click()
            # 비로그인 구매 버튼 클릭
            detail_page.buy_guest_btn_click()

            # 바로 구매 버튼 클릭 확인 (구매 페이지 진입 확인)
            wait.until(EC.url_contains("order"))
            assert "order" in driver.current_url
            logger.info("바로 구매 버튼 클릭 확인")

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

    
    ''' [단위] 장바구니 버튼 클릭 테스트 '''
    def test_cart_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품 상세페이지 진입
            driver.get(URL)

            # 상품 상세페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품 상세페이지 진입 확인")

            # 상품 옵션 클릭
            detail_page.select_option(OPTIONS[0])

            # 상품 옵션 클릭 확인
            goods_list = detail_page.save_goods_info()  # 현재 상품 정보 저장(이름, 옵션, 가격)
            assert OPTIONS[0] in goods_list[1]
            logger.info("상품 옵션 클릭 확인")

            # 장바구니 버튼 클릭
            detail_page.cart_btn_click()
            # 장바구니 확인 버튼 클릭
            detail_page.check_cart_page_btn_click()

            # 장바구니 버튼 클릭 확인 (장바구니 페이지 진입 확인)
            wait.until(EC.url_contains("basket"))
            assert "basket" in driver.current_url
            logger.info("장바구니 버튼 클릭 확인")

            # 장바구니 상품 저장 확인 (장바구니에 넣은 상품과 동일한지 확인)
            goods_table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nbg")))
            goods_name = goods_table.find_element(By.XPATH, ".//a[contains(@class, 'tb-bold')]").text
            goods_option_pull = goods_table.find_element(By.XPATH, ".//span[contains(@class, 'opt_dd')]").text
            goods_option = goods_option_pull.split(":")[1].strip().split(" ")[0]
            goods_price = goods_table.find_element(By.XPATH, ".//div[contains(@class, 'tb-price')]/span").text
            compare_goods_list = [goods_name, goods_option, goods_price]
            assert compare_goods_list == goods_list # 이름, 옵션, 가격이 전부 동일하면 PASS
            logger.info("장바구니 상품 저장 확인")

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


    ''' [단위] 관심상품 버튼 클릭 테스트 (비로그인 기준) '''
    def test_wish_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품 상세페이지 진입
            driver.get(URL)

            # 상품 상세페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품 상세페이지 진입 확인")

            # 관심상품 버튼 클릭
            detail_page.wish_btn_click()
            # 알럿 발생 시 알럿 클릭
            alert_text = utils_alert(driver)

            # 알럿 내용 확인
            assert "회원에게만 제공" in alert_text
            logger.info("비회원 알럿 내용 확인")

            # 관심상품 버튼 클릭 확인 (로그인 페이지 진입 확인)
            wait.until(EC.url_contains("member"))
            assert "member" in driver.current_url
            logger.info("관심상품 버튼 클릭 확인")

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


    ''' [단위] 상품 탭 클릭 테스트 '''
    @pytest.mark.parametrize("option_index", [0, 1, 2, 3])
    def test_goods_tab_click(self, driver: WebDriver, request, option_index):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품 상세페이지 진입
            driver.get(URL)

            # 상품 상세페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품 상세페이지 진입 확인")

            # 상품 탭 클릭
            goods_tab = detail_page.goods_tab_click(GOODS_TAB_OPTIONS[option_index])
            
            # 상품 탭 클릭 확인 (class에 active 활성화 확인)
            wait.until(lambda driver: "active" in goods_tab.get_attribute("class"))
            assert "active" in goods_tab.get_attribute("class")
            logger.info(f"{GOODS_TAB_OPTIONS[option_index]} 탭 클릭 확인")

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


    ''' [단위] 하단 스크롤 후 바로 구매 버튼 클릭 테스트 '''
    def test_fixed_buy_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            # 상품 상세페이지 진입
            driver.get(URL)

            # 상품 상세페이지 진입 확인
            wait.until(EC.url_contains(BRAND_ID))
            assert BRAND_ID in driver.current_url
            logger.info("상품 상세페이지 진입 확인")

            # 하단 스크롤 후 바로 구매 버튼 클릭
            detail_page.fixed_buy_btn_click()
            
            # 하단 스크롤 후 바로 구매 버튼 클릭 확인 (상품 옵션 선택 화면 노출 확인)
            info_fixed_check = wait.until(EC.presence_of_element_located((By.ID, "info")))
            assert info_fixed_check.is_displayed()
            logger.info("하단 스크롤 후 바로 구매 버튼 클릭 확인")

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
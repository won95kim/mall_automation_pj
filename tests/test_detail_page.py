import pytest
import os
import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv

from src.utils import utils_reports_set, utils_attach_screenshot, utils_alert
from src.detail_page import DetailPage

load_dotenv()   # env 파일 로드

# 테스트 데이터 상수 정의
GOODS_URL = os.getenv("GOODS_URL")
BRAND_ID = "70015"
OPTIONS = ["아이보리"]
GOODS_TAB_OPTIONS = ["detailGoodsInfo", "detailReview", "detailQna", "detailRelation", "detailChange"]
PAGE_NAME = "test_detail_page"

@pytest.mark.usefixtures("driver")
class TestDetailPage:

    ''' 상품 옵션 클릭 테스트 '''
    @pytest.mark.parametrize("option_index", [0])   # 상품의 옵션 수에 따라 변경
    @allure.title("상품 옵션 클릭 테스트")
    @allure.description("상품상세 페이지에서 특정 옵션을 선택하고 올바르게 선택되었는지 확인")
    def test_select_option(self, driver: WebDriver, request, option_index):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            with allure.step("상품상세 페이지 진입"):
                # 상품상세 페이지 진입
                driver.get(GOODS_URL)

            with allure.step("상품상세 페이지 진입 확인"):
                # 상품상세 페이지 진입 확인
                wait.until(EC.url_contains(BRAND_ID))
                assert BRAND_ID in driver.current_url
                logger.info("상품상세 페이지 진입 확인")

            with allure.step("상품 옵션 클릭"):
                # 상품 옵션 클릭
                detail_page.select_option(OPTIONS[option_index])

            with allure.step("상품 옵션 클릭 확인"):
                # 상품 옵션 클릭 확인
                goods_list = detail_page.save_goods_info()  # 현재 상품 정보 저장(이름, 옵션, 가격)
                assert OPTIONS[option_index] in goods_list[1]
                logger.info("상품 옵션 클릭 확인")

        except NoSuchElementException:
            logger.warning("요소를 찾을 수 없습니다. NoSuchElementException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            utils_attach_screenshot(driver, screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)
    

    ''' 바로 구매 버튼 클릭 테스트 (비로그인 기준) '''
    @allure.title("바로 구매 버튼 클릭 테스트 (비로그인)")
    @allure.description("비로그인 상태에서 바로 구매 버튼을 클릭하고 구매 페이지로 이동하는지 확인")
    def test_buy_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            with allure.step("상품상세 페이지 진입"):
                # 상품상세 페이지 진입
                driver.get(GOODS_URL)

            with allure.step("상품상세 페이지 진입 확인"):
                # 상품상세 페이지 진입 확인
                wait.until(EC.url_contains(BRAND_ID))
                assert BRAND_ID in driver.current_url
                logger.info("상품상세 페이지 진입 확인")

            with allure.step("상품 옵션 클릭"):
                # 상품 옵션 클릭
                detail_page.select_option(OPTIONS[0])

            with allure.step("상품 옵션 클릭 확인"):
                # 상품 옵션 클릭 확인
                goods_list = detail_page.save_goods_info()  # 현재 상품 정보 저장(이름, 옵션, 가격)
                assert OPTIONS[0] in goods_list[1]
                logger.info("상품 옵션 클릭 확인")

            with allure.step("바로 구매 버튼 클릭"):
                # 바로 구매 버튼 클릭
                detail_page.buy_btn_click()
                # 비로그인 구매 버튼 클릭
                detail_page.buy_guest_btn_click()

            with allure.step("바로 구매 버튼 클릭 확인"):
                # 바로 구매 버튼 클릭 확인 (구매 페이지 진입 확인)
                wait.until(EC.url_contains("order"))
                assert "order" in driver.current_url
                logger.info("바로 구매 버튼 클릭 확인")

        except NoSuchElementException:
            logger.warning("요소를 찾을 수 없습니다. NoSuchElementException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            utils_attach_screenshot(driver, screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)

    
    ''' 장바구니 버튼 클릭 테스트 '''
    @allure.title("장바구니 버튼 클릭 테스트")
    @allure.description("장바구니 버튼을 클릭하고 장바구니 페이지에서 상품 정보가 올바른지 확인")
    def test_cart_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            with allure.step("상품상세 페이지 진입"):
                # 상품상세 페이지 진입
                driver.get(GOODS_URL)

            with allure.step("상품상세 페이지 진입 확인"):
                # 상품상세 페이지 진입 확인
                wait.until(EC.url_contains(BRAND_ID))
                assert BRAND_ID in driver.current_url
                logger.info("상품상세 페이지 진입 확인")

            with allure.step("상품 옵션 클릭"):
                # 상품 옵션 클릭
                detail_page.select_option(OPTIONS[0])

            with allure.step("상품 옵션 클릭 확인"):
                # 상품 옵션 클릭 확인
                goods_list = detail_page.save_goods_info()  # 현재 상품 정보 저장(이름, 옵션, 가격)
                assert OPTIONS[0] in goods_list[1]
                logger.info("상품 옵션 클릭 확인")

            with allure.step("장바구니 버튼 클릭"):
                # 장바구니 버튼 클릭
                detail_page.cart_btn_click()
                # 장바구니 확인 버튼 클릭
                detail_page.check_cart_page_btn_click()

            with allure.step("장바구니 버튼 클릭 확인"):
                # 장바구니 버튼 클릭 확인 (장바구니 페이지 진입 확인)
                wait.until(EC.url_contains("basket"))
                assert "basket" in driver.current_url
                logger.info("장바구니 버튼 클릭 확인")

            with allure.step("장바구니 상품 저장 확인"):
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
            utils_attach_screenshot(driver, screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            utils_attach_screenshot(driver, screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)


    ''' 관심상품 버튼 클릭 테스트 (비로그인 기준) '''
    @allure.title("관심상품 버튼 클릭 테스트 (비로그인)")
    @allure.description("비로그인 상태에서 관심상품 버튼을 클릭하고 로그인 페이지로 이동하는지 확인")
    def test_wish_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            with allure.step("상품상세 페이지 진입"):
                # 상품상세 페이지 진입
                driver.get(GOODS_URL)

            with allure.step("상품상세 페이지 진입 확인"):
                # 상품상세 페이지 진입 확인
                wait.until(EC.url_contains(BRAND_ID))
                assert BRAND_ID in driver.current_url
                logger.info("상품상세 페이지 진입 확인")

            with allure.step("관심상품 버튼 클릭"):
                # 관심상품 버튼 클릭
                detail_page.wish_btn_click()
                # 알럿 발생 시 알럿 클릭
                alert_text = utils_alert(driver)

            with allure.step("알럿 내용 확인"):
                # 알럿 내용 확인
                assert "회원에게만 제공" in alert_text
                logger.info("비회원 알럿 내용 확인")

            with allure.step("관심상품 버튼 클릭 확인"):
                # 관심상품 버튼 클릭 확인 (로그인 페이지 진입 확인)
                wait.until(EC.url_contains("member"))
                assert "member" in driver.current_url
                logger.info("관심상품 버튼 클릭 확인")

        except NoSuchElementException:
            logger.warning("요소를 찾을 수 없습니다. NoSuchElementException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            utils_attach_screenshot(driver, screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)


    ''' 상품 탭 클릭 테스트 '''
    @pytest.mark.parametrize("option_index", [0, 1, 2, 3])
    @allure.title("상품 탭 클릭 테스트")
    @allure.description("상품상세 페이지에서 각 탭을 클릭하고 활성화되는지 확인")
    def test_goods_tab_click(self, driver: WebDriver, request, option_index):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            with allure.step("상품상세 페이지 진입"):
                # 상품상세 페이지 진입
                driver.get(GOODS_URL)

            with allure.step("상품상세 페이지 진입 확인"):
                # 상품상세 페이지 진입 확인
                wait.until(EC.url_contains(BRAND_ID))
                assert BRAND_ID in driver.current_url
                logger.info("상품상세 페이지 진입 확인")

            with allure.step("상품 탭 클릭"):
                # 상품 탭 클릭
                goods_tab = detail_page.goods_tab_click(GOODS_TAB_OPTIONS[option_index])
            
            with allure.step("상품 탭 클릭 확인"):
                # 상품 탭 클릭 확인 (class에 active 활성화 확인)
                wait.until(lambda driver: "active" in goods_tab.get_attribute("class"))
                assert "active" in goods_tab.get_attribute("class")
                logger.info(f"{GOODS_TAB_OPTIONS[option_index]} 탭 클릭 확인")

        except NoSuchElementException:
            logger.warning("요소를 찾을 수 없습니다. NoSuchElementException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            utils_attach_screenshot(driver, screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)


    ''' 하단 스크롤 후 바로 구매 버튼 클릭 테스트 '''
    @allure.title("하단 스크롤 후 바로 구매 버튼 클릭 테스트")
    @allure.description("상품상세 페이지에서 하단 스크롤 후 바로 구매 버튼을 클릭하고 옵션 선택 화면이 노출되는지 확인")
    def test_fixed_buy_btn_click(self, driver: WebDriver, request):
        FUNC_NAME = request.node.name   # 함수 이름 저장
        logger, screenshot = utils_reports_set(PAGE_NAME, FUNC_NAME) # 로그, 스크린샷 설정
        detail_page = DetailPage(driver)
        wait = ws(driver, 10)

        try:
            with allure.step("상품상세 페이지 진입"):
                # 상품상세 페이지 진입
                driver.get(GOODS_URL)

            with allure.step("상품상세 페이지 진입 확인"):
                # 상품상세 페이지 진입 확인
                wait.until(EC.url_contains(BRAND_ID))
                assert BRAND_ID in driver.current_url
                logger.info("상품상세 페이지 진입 확인")

            with allure.step("하단 스크롤 후 바로 구매 버튼 클릭"):
                # 하단 스크롤 후 바로 구매 버튼 클릭
                detail_page.fixed_buy_btn_click()
            
            with allure.step("하단 스크롤 후 바로 구매 버튼 클릭 확인"):
                # 하단 스크롤 후 바로 구매 버튼 클릭 확인 (상품 옵션 선택 화면 노출 확인)
                info_fixed_check = wait.until(EC.presence_of_element_located((By.ID, "info")))
                assert info_fixed_check.is_displayed()
                logger.info("하단 스크롤 후 바로 구매 버튼 클릭 확인")

        except NoSuchElementException:
            logger.warning("요소를 찾을 수 없습니다. NoSuchElementException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except TimeoutException:
            logger.warning("시간 초과 발생. TimeoutException")
            utils_attach_screenshot(driver, screenshot)
            raise
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            utils_attach_screenshot(driver, screenshot)
            raise
        finally:
            logger.info("=" * 50)
            logger.info(f"{FUNC_NAME} 테스트 완료")
            logger.info("=" * 50)
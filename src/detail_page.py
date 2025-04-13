from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class DetailPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)  # 최대 10초 대기

    ''' 상품 옵션 클릭 '''
    def select_option(self, option):
        option_dropdown = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "basic_option")))
        option_dropdown.click()
        dropdown = Select(option_dropdown)    # 드롭다운 option 선택 Select 모듈 사용
        dropdown.select_by_visible_text(option)


    ''' 바로 구매 버튼 클릭 '''
    def buy_btn_click(self):
        buy_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "바로구매")))
        buy_btn.click()
    

    ''' 비회원구매 버튼 클릭'''
    def buy_guest_btn_click(self):
        buy_guest_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "비회원구매")))
        buy_guest_btn.click()
        

    ''' 장바구니 버튼 클릭 '''
    def cart_btn_click(self):
        cart_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "cartBtn")))
        cart_btn.click()


    ''' 장바구니 확인 버튼 클릭 '''
    def check_cart_page_btn_click(self):
        check_cart_page_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "장바구니 확인")))
        check_cart_page_btn.click()


    ''' 관심상품 버튼 클릭 '''
    def wish_btn_click(self):
        wish_btn = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "관심상품")))
        wish_btn.click()
    

    ''' 상품 탭 클릭 '''
    def goods_tab_click(self, goods_tab_name):
        goods_tab = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='#{goods_tab_name}']")))
        goods_tab.click()
        return goods_tab


    ''' 하단 스크롤 후 바로 구매 버튼 클릭 '''
    def fixed_buy_btn_click(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   # 화면 최하단으로 이동
        fixed_buy_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "fixed_buy")))
        fixed_buy_btn.click()


    ''' 확인용 상품 정보 저장 '''
    def save_goods_info(self):
        goods_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tit-prd"))).text
        goods_option = self.wait.until(EC.presence_of_element_located((By.XPATH, "//li[@id='basic_0']/span"))).text
        goods_price = self.wait.until(EC.presence_of_element_located((By.ID, "MK_p_total"))).text
        goods_list = [goods_title, goods_option, goods_price]
        return goods_list
    
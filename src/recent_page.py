from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC

class RecentPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = ws(driver, 10)  # 최대 10초 대기

    ''' 상품 정보 저장 '''
    def save_goods_info(self):
        goods_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tit-prd"))).text
        goods_price = self.wait.until(EC.presence_of_element_located((By.XPATH, "//td[@class='price sell_price']/div"))).text
        goods_list = [goods_title, goods_price]
        return goods_list

    ''' 오늘 본 상품 정보 저장 '''
    def save_today_goods_info(self):
        goods_title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dsc"))).text
        goods_price = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price_1"))).text
        today_goods_list = [goods_title, goods_price]
        return today_goods_list
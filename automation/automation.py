from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


class SeleniumService:
    def __init__(self):
        self.driver = None

    def initialize(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--user-data-dir=C:\\chromeCookie")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(3)

    # 로그인
    def login(self, username, password):
        self.driver.get("https://www.coupang.com/")
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="login"]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="login-email-input"]').send_keys(
            username
        )
        self.driver.find_element(By.XPATH, '//*[@id="login-password-input"]').send_keys(
            password
        )
        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/form/div[5]/button"
        ).click()
        time.sleep(1)

    # 상품 이동
    def goToProduct(self, product_url):
        self.driver.get(product_url)
        cart_button = self.driver.find_elements(
            By.XPATH,
            "/html/body/div[2]/section/div/div[1]/div[3]/div[17]/div[2]/div[2]/button[1]",
        )[0]
        cart_button.click()
        time.sleep(1)

    # 장바구니 이동
    def goToCart(self):
        cart_button = self.driver.find_elements(
            By.XPATH, '//*[@id="header"]/section/div[1]/ul/li[2]/a'
        )[0]
        cart_button.click()
        time.sleep(1)

    # 장바구니에 있는 모든 상품 선택
    def selectAllItemsInCart(self):
        cart_all_select_button = self.driver.find_elements(
            By.XPATH, '//*[@id="cartContent"]/table/thead/tr/th[1]/label/input'
        )[0]
        is_selected = cart_all_select_button.is_selected()
        time.sleep(1)

        if is_selected == False:
            cart_all_select_button.click()
            self.driver.implicitly_wait(1)
        time.sleep(1)

    # 장바구니에서 결제하기 버튼 클릭
    def clickBuyButton(self):
        buy_button = self.driver.find_elements(By.XPATH, '//*[@id="btnPay"]')[0]
        print(buy_button)
        buy_button.click()
        time.sleep(1)

    # 결제하기 버튼 클릭
    def clickPayButton(self):
        payment_button = self.driver.find_elements(
            By.XPATH, '//*[@id="paymentBtn"]/img'
        )[0]
        payment_button.click()
        time.sleep(1)

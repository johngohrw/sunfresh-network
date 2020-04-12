from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from random import randint
import time
import datetime

#===================================
# VARIABLES
#===================================

chrome_driver_path = './drivers/chromedriver'
username_credentials = 'andyyap@sunfresh.my'
password_credentials = 'Sunfresh2020'
shopify_store_name = 'wefresh-by-webay-group'

#===================================


class SeleniumController():
    def __init__(self):
        self.debug = True
        self.page_load_delay = 5
        self.browser = webdriver.Chrome(chrome_driver_path)
        self.browser.set_page_load_timeout(30)

        isloggedin = False
        while not isloggedin:
            isloggedin = self.shopify_login()
            if not isloggedin:
                print("not logged in.. trying again")


    def shopify_login(self):
        url = 'https://{}.myshopify.com/admin'.format(shopify_store_name)
        if self.debug: print("[Selenium] loading {} ..".format(url))
        self.browser.get(url)
        try:
            elem = WebDriverWait(self.browser, self.page_load_delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.next-input.email-typo-input')))
        except TimeoutError:
            print("[Selenium] Login took too much time!")
            return False
        print(self.browser.current_url)
        # assert "Shopify" in self.browser.getU

        return True


if __name__ == "__main__":
    c = SeleniumController()

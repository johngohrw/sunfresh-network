from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import os
from pyvirtualdisplay import Display
from dotenv import load_dotenv
from fake_useragent import UserAgent
load_dotenv()

# VARIABLES
chrome_driver_path = './drivers/chromedriver_{}'.format(os.getenv('HOST_OS'))
username_credentials = os.getenv('SHOPIFY_LOGIN_EMAIL')
password_credentials = os.getenv('SHOPIFY_LOGIN_PASSWORD')
shopify_store_name = os.getenv('SHOPIFY_STORE_NAME')


class SeleniumController:
    def __init__(self):
        self.page_load_delay = 5
        self.page_load_interval = 5
        self.action_interval = 5
        self.wait_timeout = 20
        self.debug = True

        # uninitialized variables
        self.virtual_display = None
        self.browser = None

    def login_all(self):
        # login to shopify and secomapp
        login = self.shopify_login()
        assert login
        login = self.secomapp_login()
        assert login
        return True

    def start_browser(self):
        self.debug_print("Loading webdriver from {}".format(chrome_driver_path))
        # starts xvfb virtual display for linux servers without an actual display output
        if os.getenv('ENABLE_VIRTUAL_DISPLAY') == '1':
            self.debug_print('Starting pyvirtualdisplay')
            self.virtual_display = Display(visible=0, size=(1243, 722))
            self.virtual_display.start()



        # add headless arguments if HEADLESS env variable is set to 1
        chrome_options = Options()

        if os.getenv('HEADLESS') == '1':
            self.debug_print('Running Chrome in headless mode')
            # ua = UserAgent()
            # chrome_options.add_argument(f'user-agent={ua.random}')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        return True

    def close_browser(self):
        self.browser.close()
        self.debug_print("Browser closed")
        if os.getenv('ENABLE_VIRTUAL_DISPLAY') == '1':
            self.virtual_display.stop()
        return True

    # Shopify login process
    def shopify_login(self):
        self.debug_print("Starting Shopify login")
        self.load_page('https://{}.myshopify.com/admin'.format(shopify_store_name))

        # let the page load
        time.sleep(self.page_load_delay)

        # wait for email field
        try:
            elem = WebDriverWait(self.browser, self.wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.next-input.email-typo-input')))
        except TimeoutException:
            self.debug_print("Loading login page took too much time!")
            return False
        assert "accounts.shopify.com" in self.browser.current_url

        # Page load success, input email
        self.debug_print("Inputting email")

        for i in range(len(username_credentials)):
            comment = self.browser.find_element_by_xpath("//input[@id='account_email']")
            comment.send_keys(username_credentials[i])
            time.sleep(0.7)

        self.debug_print("Email input done")

        next_elem = self.browser.find_element_by_xpath("//button[@type='submit']")
        print(next_elem.screenshot_as_base64)

        try:
            newelem = WebDriverWait(self.browser, self.wait_timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        except TimeoutException:
            self.debug_print("Next elem not clickable!")
            # print(newelem.screenshot_as_base64)
            return False

        next_elem = self.browser.find_element_by_xpath("//button[@type='submit']")
        # print(newelem.screenshot_as_base64)
        next_elem.click()

        # Wait for password field
        try:
            elem = WebDriverWait(self.browser, self.wait_timeout).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='account[password]']")))
        except TimeoutException:
            self.debug_print("Password field took too much time!")
            return False

        # Input password
        self.debug_print("Inputting password")
        pass_elem = self.browser.find_element_by_xpath("//input[@name='account[password]']")
        next_elem = self.browser.find_element_by_xpath("//button[@type='submit'][@name='commit']")

        self.debug_print("Logging in..")

        ActionChains(self.browser) \
            .move_to_element(pass_elem).click() \
            .send_keys(password_credentials) \
            .perform()
        next_elem.click()

        # let the page load
        time.sleep(self.page_load_delay)

        # check if properly signed in
        try:
            elem = WebDriverWait(self.browser, self.wait_timeout).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='search'][@placeholder='Search']")))
        except TimeoutException:
            self.debug_print("Logging into Shopify took too much time!")
            return False
        print("Shopify Login Success!")
        return True

    # Secomapp login process
    def secomapp_login(self):
        self.debug_print("Starting Secomapp login")
        self.load_page('https://af.secomapp.com/login')

        # wait for email field
        try:
            elem = WebDriverWait(self.browser, self.wait_timeout).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='shop'][@placeholder='shop name']")))
        except TimeoutException:
            self.debug_print("Loading login page took too much time!")
            return False

        # Page load success, input email
        self.debug_print("Inputting shop name")
        shop_name_elem = self.browser.find_element_by_xpath("//input[@name='shop'][@placeholder='shop name']")
        next_elem = self.browser.find_element_by_xpath("//button[@type='submit'][text() = 'Login']")

        self.debug_print("Logging in..")

        ActionChains(self.browser) \
            .move_to_element(shop_name_elem).click() \
            .send_keys(shopify_store_name) \
            .perform()
        next_elem.click()

        # let the page load
        time.sleep(self.page_load_delay)

        # check if properly signed in
        try:
            elem = WebDriverWait(self.browser, self.wait_timeout).until(
                EC.presence_of_element_located((By.XPATH, "//title[text()='Dashboard']")))
        except TimeoutException:
            self.debug_print("Logging into Secomapp took too much time!")
            return False
        print("Secomapp Login Success!")
        return True

    def debug_print(self, string):
        prefix = "[Selenium] "
        if self.debug: print(prefix + string)

    def load_page(self, url):
        self.debug_print("Loading page: {}".format(url))
        self.browser.get(url)
        self.debug_print("Loaded successfully!")
        time.sleep(self.page_load_interval)


if __name__ == "__main__":
    print("SeleniumController debug run")
    c = SeleniumController()
    c.start_browser()
    c.login_all()
    c.close_browser()

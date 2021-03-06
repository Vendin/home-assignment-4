from urlparse import urlparse, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Page:
    BASE_URL = 'https://target.my.com/'
    PATH = ''
    HDR_XPATH = ''

    def __init__(self, driver):
        self.driver = driver
        self.window_handle = driver.current_window_handle

    def open(self):
        url = urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait_for_load()

    def wait_for_load(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.HDR_XPATH))
            )
        except TimeoutException:
            print "No header found"

    def check_element_exists(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def close(self):
        self.driver.close()

class Component(object):
    def __init__(self, driver):
        self.driver = driver

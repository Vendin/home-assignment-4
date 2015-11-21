from urlparse import urlparse, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def check_visible(xpath, driver, ttl=2):
    try:
        WebDriverWait(driver, ttl).until(
            EC.visibility_of_element_located((
                By.XPATH, xpath
            ))
        )
        return True
    except TimeoutException:
        return False

def check_invisible(xpath, driver, ttl=2):
    try:
        WebDriverWait(driver, ttl).until(
            EC.invisibility_of_element_located((
                By.XPATH, xpath
            ))
        )
        return True
    except TimeoutException:
        return False

class Page:
    BASE_URL = 'https://target.my.com/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver
        self.window_handle = driver.current_window_handle

    def open(self):
        url = urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait_for_load()
    
    def wait_for_load(self):
        return

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

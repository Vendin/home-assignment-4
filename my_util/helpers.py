from urlparse import urlparse, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from page.page import Page

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

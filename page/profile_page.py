__author__ = 'av'

from page import Page
from my_util.helpers import check_visible
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProfilePage(Page):
    PATH = '/profile/'

    HDR_XPATH = '//div[contains(@class, "base-form__title")]'
    INPUT_FIO = '//input[contains(@data-name, "fio")]'
    INPUT_INFO = '//input[contains(@data-name, "phone")]'
    INPUT_EMAIL  = '//input[contains(@data-name, "email")]'
    BUTTON_SUBMIT = '//input[contains(@data-type, "save")]'
    MESSAGE_OK = '//div[contains(@class, "base-form__response")]'

    def wait_for_load(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.HDR_XPATH))
            )
        except TimeoutException:
            print "No header found"

    def get_profile(self, info):
        input = self.driver.find_element_by_xpath(info)
        return input.get_attribute('value')

    def edit_prolfile(self, info,  name = "Anton"):
        input = self.driver.find_element_by_xpath(info)
        input.clear()
        input.send_keys(name)

    def edit_save(self):
        button = self.driver.find_element_by_xpath(self.BUTTON_SUBMIT)
        button.click()
        check_visible(ProfilePage.MESSAGE_OK, self.driver, 5)


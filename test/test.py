# -*- coding: utf-8 -*-
__author__ = 'av'


import os
import unittest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from urlparse import urlparse, urljoin



class Page:
    BASE_URL = 'https://target.my.com/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()

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

class MainPage(Page):
    PATH = ''

    LOGIN_BTN_XPATH = '//span[contains(@class, "ph-button__inner_profilemenu_signin")]'
    MENU_BTN_XPATH = '//span[@xname="clb2490734"]'

    INTERNAL_URL = 'https://target.my.com/ads/campaigns/'
    INTERNAL_ELEMENT_XPATH = '//*[contains(@class, "campaign-toolbar__create-button")]'

    @property
    def login_button(self):
        return Button(self.driver, self.LOGIN_BTN_XPATH)

    def login_button_exists(self):
        return Page.check_element_exists(self, self.LOGIN_BTN_XPATH)

    @property
    def menu_button(self):
        return Button(self.driver, self.MENU_BTN_XPATH)

    def menu_button_exists(self):
        return Page.check_element_exists(self, self.MENU_BTN_XPATH)

    def login_mail(self):
        self.login_button.click()
        login_menu = AuthoriseMenu(self.driver)
        login_menu.click_mail()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.INTERNAL_ELEMENT_XPATH)
                )
            )
            return True
        except TimeoutException:
            return False

    def open(self):
        Page.open(self)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.LOGIN_BTN_XPATH))
            )
        except TimeoutException:
            print "No login button found"

class Button(Component):
    def __init__(self, driver, xpath):
        Component.__init__(self, driver)
        self.xpath = xpath
        self.button = self.driver.find_element_by_xpath(self.xpath)

    def click(self):
        self.button.click()

class AuthoriseMenu(Component):
    MAIL_XPATH = '//span[contains(@class, "mycom-auth__social-icon_mail")]'

    def __init__(self, driver):
        Component.__init__(self, driver)
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((
                By.XPATH, self.MAIL_XPATH
            ))
        )

    def click_mail(self):
        mail_button = self.driver.find_element_by_xpath(self.MAIL_XPATH)
        mail_button.click()

class TargetTest(unittest.TestCase):
    USERNAME = u'name'

    def setUp(self):
        browser = os.environ.get('TTHA4BROWSER', 'FIREFOX')
        self.password = os.environ.get('TTHA4PASSWORD')
        self.login = os.environ.get('TTHA4LOGIN')
        self.mode = os.environ.get('TTHA4MODE', 'mail')

        if browser == 'CHROME':
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()
        """
        This is for grid
        self.driver = Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        """
        self.main_page = MainPage(self.driver)
        self.main_page.open()


    def tearDown(self):
        self.main_page.close()
        self.driver.quit()

    def test_login_button_present(self):
        self.assertTrue(self.main_page.login_button_exists())

    def test_menu_button_present(self):
        self.assertTrue(self.main_page.menu_button_exists())

    def test_login_mail(self):
        self.assertTrue(self.main_page.login_mail())

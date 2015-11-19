# -*- coding: utf-8 -*-
__author__ = 'av'


import os
import unittest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

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

    def close(self):
        self.driver.close()

class Component(object):
    def __init__(self, driver):
        self.driver = driver

class MainPage(Page):
    PATH = ''

    @property
    def login_button(self):
        return LoginButton(self.driver)

    def open(self):
        Page.open(self)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH,
                LoginButton.XPATH))
        )

class LoginButton(Component):
    XPATH = '//span[contains(@class, "ph-button__inner_profilemenu_signin")]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.XPATH).click()


class TargetTest(unittest.TestCase):
    USERNAME = u'name'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        self.main_page = MainPage(self.driver)
        self.main_page.open()


    def test(self):
        login_button = self.main_page.login_button
        login_button.open_form()
        self.assertEqual(3, 1)

    def tearDown(self):
        self.main_page.close()


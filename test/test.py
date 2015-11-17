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
        print(1)
        url = urljoin(self.BASE_URL, self.PATH)
        print(1.5, url)
        self.driver.get(url)
        print(2)
        self.driver.maximize_window()

class Component(object):
    def __init__(self, driver):
        self.driver = driver

class AuthPage(Page):
    PATH = ''

    def form(self):
        return AuthForm(self.driver)

    def open(self):
        Page.open(self)
        print('start wait')
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, AuthForm.LOGIN_BUTTON))
        )
        print('end wait')

class AuthForm(Component):
    LOGIN_BUTTON = '//span[contains(@class, "ph-button__inner_profilemenu_signin")]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()


class TargetTest(unittest.TestCase):
    USERNAME = u'name'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )


    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form()
        auth_form.open_form()
        self.assertEqual(3, 1)


__author__ = 'av'


import os
import unittest
from selenium import webdriver


class Page:
    BASE_URL = 'https://target.my.com/'
    PATH = ''

    def __init__(self):
        self.driver = driver

    def open(self):
        self.driver = webdriver.Firefox()
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()

class Component(object):
    def __init__(self, driver):
        self.driver = driver

class AuthPage(Page):
    PATH = ''

    def setUp(self):

    @property
    def form(self):
        return AuthForm(self.driver)

class AuthForm(Component):
    LOGIN_BUTTON = '//span[text()="Log In"]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()


class TargetTest(unittest.TestCase):
    USERNAME = u'name'
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')



    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        self.assertEqual(3, 1)


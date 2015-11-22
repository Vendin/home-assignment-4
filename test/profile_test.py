
import os
import unittest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from helpers import Page, Component, check_visible, check_invisible
from main_page import MainPage
from test import TargetTest

class ProfilePage(Page):
    PATH = '/profile/'

    HDR_XPATH = '//div[contains(@class, "base-form__title")]'
    INPUT_FIO = '//input[contains(@data-name, "fio")]'


    def edit_FIO(self, name = "Anton"):
        input = self.driver.find_element_by_xpath(self.INPUT_FIO)
        input.clear()
        input.send_keys(name)

class TargetTestProfile(TargetTest):

    def open(self):
        self.page = ProfilePage(self.driver)
        self.page.open()

    def test_rename(self):
            self.page.edit_FIO()
            self.assertTrue(True)

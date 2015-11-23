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
from helpers import check_visible

class ProfilePage(Page):
    PATH = '/profile/'

    HDR_XPATH = '//div[contains(@class, "base-form__title")]'
    INPUT_FIO = '//input[contains(@data-name, "fio")]'
    INPUT_INFO = '//input[contains(@data-name, "phone")]'
    INPUT_EMAIL  = '//input[contains(@data-name, "email")]'
    BUTTON_SUBMIT = '//input[contains(@data-type, "save")]'
    MESSAGE_OK = '//div[contains(@class, "base-form__response")]'

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

class TargetTestProfile(TargetTest):

    def open(self):
        self.page = ProfilePage(self.driver)
        self.page.open()

    def test_rename(self):
            name = self.page.get_profile(ProfilePage.INPUT_FIO)
            self.page.edit_prolfile(ProfilePage.INPUT_FIO, "Name")
            self.page.edit_save()
            self.driver.refresh()
            check_visible(ProfilePage.BUTTON_SUBMIT, self.driver, 5)
            self.assertEquals(self.page.get_profile(ProfilePage.INPUT_FIO), "Name")
            self.page.edit_prolfile(ProfilePage.INPUT_FIO, name)
            self.page.edit_save()

    def test_reinfo(self):
            info = self.page.get_profile(ProfilePage.INPUT_INFO)
            self.page.edit_prolfile(ProfilePage.INPUT_INFO, "Info")
            self.page.edit_save()
            self.driver.refresh()
            check_visible(ProfilePage.BUTTON_SUBMIT, self.driver, 5)
            self.assertEquals(self.page.get_profile(ProfilePage.INPUT_INFO), "Info")
            self.page.edit_prolfile(ProfilePage.INPUT_INFO, info)
            self.page.edit_save()

    def test_reemail(self):
            email = self.page.get_profile(ProfilePage.INPUT_EMAIL)
            self.page.edit_prolfile(ProfilePage.INPUT_EMAIL, "Mail")
            self.page.edit_save()
            self.driver.refresh()
            check_visible(ProfilePage.BUTTON_SUBMIT, self.driver, 5)
            self.assertEquals(self.page.get_profile(ProfilePage.INPUT_EMAIL), "Mail")
            self.page.edit_prolfile(ProfilePage.INPUT_EMAIL, email)
            self.page.edit_save()

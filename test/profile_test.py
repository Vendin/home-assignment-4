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

from page import page
from page import main_page
from test import TargetTest
from my_util.helpers import check_visible
from page.page import Page
from page.profile_page import ProfilePage
from selenium.common.exceptions import TimeoutException

class TargetTestProfile(TargetTest):

    def open(self):
        self.page = ProfilePage(self.driver)
        self.page.open()

    def setUp(self):
          TargetTest.setUp(self)
          self.name = self.page.get_profile(ProfilePage.INPUT_FIO)
          self.info = self.page.get_profile(ProfilePage.INPUT_INFO)
          self.email = self.page.get_profile(ProfilePage.INPUT_EMAIL)

    def tearDown(self):
            self.page.edit_prolfile(ProfilePage.INPUT_FIO, self.name)
            self.page.edit_prolfile(ProfilePage.INPUT_INFO, self.info)
            self.page.edit_prolfile(ProfilePage.INPUT_EMAIL, self.email)
            self.page.edit_save()
            TargetTest.tearDown(self)

    def test_rename(self):
            self.page.edit_prolfile(ProfilePage.INPUT_FIO, "Name")
            self.page.edit_save()
            self.driver.refresh()
            check_visible(ProfilePage.BUTTON_SUBMIT, self.driver, 5)
            self.assertEquals(self.page.get_profile(ProfilePage.INPUT_FIO), "Name")

    def test_reinfo(self):
            self.page.edit_prolfile(ProfilePage.INPUT_INFO, "Info")
            self.page.edit_save()
            self.driver.refresh()
            check_visible(ProfilePage.BUTTON_SUBMIT, self.driver, 5)
            self.assertEquals(self.page.get_profile(ProfilePage.INPUT_INFO), "Info")

    def test_reemail(self):
            self.page.edit_prolfile(ProfilePage.INPUT_EMAIL, "Mail")
            self.page.edit_save()
            self.driver.refresh()
            check_visible(ProfilePage.BUTTON_SUBMIT, self.driver, 5)
            self.assertEquals(self.page.get_profile(ProfilePage.INPUT_EMAIL), "Mail")

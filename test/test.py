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

from helpers import Page, Component
from main_page import MainPage


class AudiencePage(Page):
  PATH = '/ads/audience/'
  
  HDR_XPATH = '//h3[contains(@class, "audience-page__title")]'
  
  BTN_XPATH_TMPL = '//ul[contains(@class, "sources-nav")]/li[%i]/span[1]'
  TOP_BTN_XPATH = BTN_XPATH_TMPL % 1
  OK_BTN_XPATH = BTN_XPATH_TMPL % 2
  VK_BTN_XPATH = BTN_XPATH_TMPL % 3
  OKAPP_BTN_XPATH = BTN_XPATH_TMPL % 4
  VKAPP_BTN_XPATH = BTN_XPATH_TMPL % 5
  USRLIST_BTN_XPATH = BTN_XPATH_TMPL % 6
  SRCHLIST_BTN_XPATH = BTN_XPATH_TMPL % 7
  PRICELST_BTN_XPATH = BTN_XPATH_TMPL % 8
  
  def get_top_ctr_adder(self):
    top_btn = self.driver.find_element_by_xpath(self.TOP_BTN_XPATH)
    top_btn.click()
    return TopCtrAdder(self.driver)
  
  def wait_for_load(self):
      try:
          WebDriverWait(self.driver, 10).until(
              EC.presence_of_element_located((By.XPATH, self.HDR_XPATH))
          )
      except TimeoutException:
          print "No header found"
    

class TopCtrAdder(Component):
  INPUT_XPATH = '//span[@data-name="remarketingCounter"]/parent::*/following-sibling::input'
  ADD_BTN_XPATH = '//span[@data-name="remarketingCounter"]/ancestor::div[@class="source-form"]/descendant::input[@type="submit"]'
  ERR_MSG_XPATH = '//div[@class="source-form__error js-counter-form-error"]'
  
  def add_ctr(self, ctr_id):
    input = self.driver.find_element_by_xpath(self.INPUT_XPATH)
    add_btn = self.driver.find_element_by_xpath(self.ADD_BTN_XPATH)
    input.send_keys(str(ctr_id))
    add_btn.click()
  
  def check_has_error(self):
    try:
        WebDriverWait(self.driver, 2).until(
            EC.visibility_of_element_located((
                By.XPATH, self.ERR_MSG_XPATH
            ))
        )
        return True
    except TimeoutException:
        return False

class TargetTest(unittest.TestCase):
    USERNAME = u'name'
    
    @classmethod
    def setUpClass(cls):
      cls.browser = os.environ.get('TTHA4BROWSER', 'FIREFOX')
      cls.password = os.environ.get('TTHA4PASSWORD', 'password')
      cls.login = os.environ.get('TTHA4LOGIN', 'login')
      cls.mode = os.environ.get('TTHA4MODE', 'mail')


    def setUp(self):
        if TargetTest.browser == 'CHROME': self.driver = webdriver.Chrome()
        else: self.driver = webdriver.Firefox()
        """
        This is for grid
        self.driver = Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        """
        main_page = MainPage(self.driver)
        main_page.open()
        main_page.login_mail(TargetTest.login, TargetTest.password)
        self.page = AudiencePage(self.driver)
        self.page.open()


    def tearDown(self):
        self.page.close()
        self.driver.quit()
    
    def test_ctr_filters_input(self):
        wrong_ctr_id = 123
        top_ctr_adder = self.page.get_top_ctr_adder();
        top_ctr_adder.add_ctr(wrong_ctr_id)
        self.assertTrue(top_ctr_adder.check_has_error())

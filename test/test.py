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
        self.window_handle = driver.current_window_handle

    def open(self):
        url = urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait_for_load()
    
    def wait_for_load(self):
        return

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
      
    def get_popup(self, driver):
      popup_handle = None
      for handle in driver.window_handles:
          if handle != self.window_handle:
              popup_handle = handle
              break
      return popup_handle

    def login_mail(self, username, password):
        self.login_button.click()
        login_menu = AuthorizeMenu(self.driver)
        popup_handle = None
        login_menu.click_mail()
        popup_handle = WebDriverWait(self.driver, 10).until(
          self.get_popup
        )
        mail_auth = MailAuthorize(self.driver, popup_handle, self.window_handle)
        mail_auth.login(username, password)
        
        return self.wait_for_internal_loaded()
    
    def wait_for_internal_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.INTERNAL_ELEMENT_XPATH)
                )
            )
            return True
        except TimeoutException:
            return False

    def wait_for_load(self):
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

class AuthorizeMenu(Component):
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

class MailAuthorize(Component):
    LOGIN_XPATH = '//*[@id="login"]'
    PASSWORD_XPATH = '//*[@id="password"]'
    SUBMIT_XPATH = '//button[@type="submit"]'
    
    def __init__(self, driver, popup_handle, window_handle):
        Component.__init__(self, driver)
        self.window_handle = window_handle
        self.popup_handle = popup_handle
        self.driver.switch_to.window(self.popup_handle)
        self.login_input = driver.find_element_by_xpath(self.LOGIN_XPATH)
        self.password_input = driver.find_element_by_xpath(self.PASSWORD_XPATH)
        self.submit_button = driver.find_element_by_xpath(self.SUBMIT_XPATH)
        self.driver.switch_to.window(self.window_handle)
    
    def login(self, username, password):
        self.driver.switch_to.window(self.popup_handle)
        self.login_input.send_keys(username)
        self.password_input.send_keys(password)
        self.submit_button.click()   
        self.driver.switch_to.window(self.window_handle)

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

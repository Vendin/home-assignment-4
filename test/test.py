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
from selenium.webdriver.common.action_chains import ActionChains

from helpers import Page, Component, check_visible, check_invisible
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
    
    def get_ok_group_adder(self):
        ok_btn = self.driver.find_element_by_xpath(self.OK_BTN_XPATH)
        ok_btn.click()
        return OKGroupAdder(self.driver)
    
    def get_vk_group_adder(self):
        ok_btn = self.driver.find_element_by_xpath(self.VK_BTN_XPATH)
        ok_btn.click()
        return VKGroupAdder(self.driver)
    
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
    
    TOP_CTR_ID_XPATH_TMPL = '//ul[@class="sources-list__list-wrapper js-list-wrapper"]/descendant::span[@class="source-list-item__id" and text()="%i"]'
    
    def add_ctr(self, ctr_id):
        input = self.driver.find_element_by_xpath(self.INPUT_XPATH)
        add_btn = self.driver.find_element_by_xpath(self.ADD_BTN_XPATH)
        input.send_keys(str(ctr_id))
        add_btn.click()
        self.check_has_ctr(ctr_id)
    
    def check_has_error(self):
        return check_visible(self.ERR_MSG_XPATH, self.driver)
    
    def check_has_ctr(self, id):
        return check_visible(self.TOP_CTR_ID_XPATH_TMPL % id, self.driver)
            
    def _wait_no_ctr(self, id):
        return check_invisible(self.TOP_CTR_ID_XPATH_TMPL % id, self.driver)
    
    def delete_ctr(self, id):
        id_xpath = self.TOP_CTR_ID_XPATH_TMPL % id
        li_xpath = id_xpath + '/parent::li'
        
        li = self.driver.find_element_by_xpath(li_xpath)
        del_xpath = li_xpath + '/span[contains(@class, "source-list-item__delete")]'
        delete = self.driver.find_element_by_xpath(del_xpath)
        
        self.driver.execute_script(
          """arguments[0].style.visibility='visible';
             arguments[0].style.display='block';""",
          delete
        )
        delete.click()
        self._wait_no_ctr(id)
        
class GroupAdder(Component):
    INPUT_XPATH = '//input[contains(@class, "suggester__input") and not(ancestor::*[contains(@style, "display: none")])]'
    HELPER_XPATH = INPUT_XPATH+'/following-sibling::div[contains(@class, "suggester__list")]'
    
    def input_group(self, group):
        group_input = self.driver.find_element_by_xpath(self.INPUT_XPATH)
        group_input.send_keys(group)
    
    def check_has_helper(self):
        return check_visible(self.HELPER_XPATH, self.driver)
        
class OKGroupAdder(GroupAdder):
    pass

class VKGroupAdder(GroupAdder):
    def check_has_helper(self):
        return check_visible(self.HELPER_XPATH, self.driver, ttl=5)
    
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
        wrong_ctr_id = 0
        top_ctr_adder = self.page.get_top_ctr_adder()
        top_ctr_adder.add_ctr(wrong_ctr_id)
        self.assertTrue(top_ctr_adder.check_has_error())
    
    def test_ctr_adds(self):
        right_ctr_id = 240
        top_ctr_adder = self.page.get_top_ctr_adder()
        top_ctr_adder.add_ctr(right_ctr_id)
        self.assertTrue(top_ctr_adder.check_has_ctr(right_ctr_id))
        top_ctr_adder.delete_ctr(right_ctr_id)
    
    def test_ctr_deletes(self):
        right_ctr_id = 240
        top_ctr_adder = self.page.get_top_ctr_adder()
        top_ctr_adder.add_ctr(right_ctr_id)
        top_ctr_adder.delete_ctr(right_ctr_id)
        self.assertFalse(top_ctr_adder.check_has_ctr(right_ctr_id))
    
    def test_ok_ctr_has_helper(self):
        ok_theme = "Sport"
        ok_ctr_adder = self.page.get_ok_group_adder()
        ok_ctr_adder.input_group(ok_theme)
        self.assertTrue(ok_ctr_adder.check_has_helper())
    
    def test_ok_ctr_filters_wrong(self):
        ok_strange_theme = "asdfsdfsdfsdfasdf12312@as2"
        ok_ctr_adder = self.page.get_ok_group_adder()
        ok_ctr_adder.input_group(ok_strange_theme)
        self.assertFalse(ok_ctr_adder.check_has_helper())
    
    def test_vk_ctr_has_helper(self):
        vk_group = "Sport"
        vk_ctr_adder = self.page.get_vk_group_adder()
        vk_ctr_adder.input_group(vk_group)
        self.assertTrue(vk_ctr_adder.check_has_helper())
    
    def test_ok_ctr_filters_wrong(self):
        vk_strange_theme = "asdfsdfsdfsdfasdf12312@as2"
        vk_ctr_adder = self.page.get_vk_group_adder()
        vk_ctr_adder.input_group(vk_strange_theme)
        self.assertFalse(vk_ctr_adder.check_has_helper())

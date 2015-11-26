# -*- coding: utf-8 -*-
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

from my_util.helpers import  check_visible, check_invisible
from main_page import MainPage
from test.test import TargetTest
from page import Page, Component



class AudiencePage(Page):
    PATH = '/ads/audience/'

    HDR_XPATH = '//h3[contains(@class, "audience-page__title")]'

    BTN_XPATH_TMPL = '//ul[contains(@class, "sources-nav")]/li[%i]/span[1]'
    TOP_BTN_XPATH      = BTN_XPATH_TMPL % 1
    OK_BTN_XPATH       = BTN_XPATH_TMPL % 2
    VK_BTN_XPATH       = BTN_XPATH_TMPL % 3
    OKAPP_BTN_XPATH    = BTN_XPATH_TMPL % 4
    VKAPP_BTN_XPATH    = BTN_XPATH_TMPL % 5
    USRLIST_BTN_XPATH  = BTN_XPATH_TMPL % 6
    SRCHLIST_BTN_XPATH = BTN_XPATH_TMPL % 7
    PRICELST_BTN_XPATH = BTN_XPATH_TMPL % 8

    AUD_CREATE_BTN_XPATH = '//input[contains(@class, "audience-page__audience-create-submit")]'

    def get_top_ctr_adder(self):
        top_btn = self.driver.find_element_by_xpath(self.TOP_BTN_XPATH)
        top_btn.click()
        return TopCtrAdder(self.driver)

    def get_ok_group_adder(self):
        check_visible(self.OK_BTN_XPATH, self.driver)
        ok_btn = self.driver.find_element_by_xpath(self.OK_BTN_XPATH)
        ok_btn.click()
        return OKGroupAdder(self.driver)

    def get_vk_group_adder(self):
        check_visible(self.VK_BTN_XPATH, self.driver)
        vk_btn = self.driver.find_element_by_xpath(self.VK_BTN_XPATH)
        vk_btn.click()
        return VKGroupAdder(self.driver)

    def get_vk_app_adder(self):
        vk_app_btn = self.driver.find_element_by_xpath(self.VKAPP_BTN_XPATH)
        vk_app_btn.click()
        return VKAppAdder(self.driver)

    def wait_for_load(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.HDR_XPATH))
            )
        except TimeoutException:
            print "No header found"

    def has_create_aud_btn(self):
        return check_visible(self.AUD_CREATE_BTN_XPATH, self.driver)

    def get_create_aud_form(self):
        create_aud_btn = self.driver.find_element_by_xpath(self.AUD_CREATE_BTN_XPATH)
        create_aud_btn.click()
        aud_form = AudienceForm(self.driver)
        check_visible(aud_form.FORM_XPATH, self.driver)
        return aud_form

    def get_aud_element(self, name):
        if check_visible(AudienceElement.HDR_XPATH_TMPL % name, self.driver, ttl=7):
            return AudienceElement(self.driver, name);
        else:
            return None


class TopCtrAdder(Component):
    INPUT_XPATH = '//input[contains(@class, "js-counter-form-input")]'
    ADD_BTN_XPATH = '//input[contains(@class,"js-counter-form-add")]'
    ERR_MSG_XPATH = '//div[@class="source-form__error js-counter-form-error"]'

    TOP_CTR_ID_XPATH_TMPL = '//ul[contains(@class, "js-list-wrapper")]/descendant::span[@class="source-list-item__id" and text()="%i"]'

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

class VKAppAdder(GroupAdder):
    def check_has_helper(self):
        return check_visible(self.HELPER_XPATH, self.driver, ttl=5)

class AudienceForm(Component):
    FORM_XPATH = '//*[contains(@class, "audience-form")][1]'

    def __init__(self, driver, xpath=None):
        if xpath is None:
            xpath = AudienceForm.FORM_XPATH
        Component.__init__(self, driver)
        self._SELF_XPATH = xpath

        self._NAME_XPATH = self._SELF_XPATH+'/descendant::input[contains(@class, "audience-form__audience-name-input")]'
        self._SUBMIT_XPATH = self._SELF_XPATH+'/descendant::input[@type="submit"]'
        self._DELETE_XPATH = self._SELF_XPATH+'/descendant::span[contains(@class, "audience-form__delete")]'
        self._DEL_YES_XPATH = self._SELF_XPATH+'/descendant::input[contains(@class, "audience-form__confirm-button") and @data-type="yes"]';

        self._MARK_ALL_XPATH = self._SELF_XPATH+'/descendant::input[@id="-box-all"]'

        self._SOURCE_ERR_XPATH = self._SELF_XPATH + '/descendant::div[contains(@class, "audience-form__no-source-error")]'

    def input_name(self, name):
        check_visible(self._NAME_XPATH, self.driver)
        name_input = self.driver.find_element_by_xpath(self._NAME_XPATH)
        name_input.clear()
        name_input.send_keys(name)

    def mark_all(self):
        mark_all_radio = self.driver.find_element_by_xpath(self._MARK_ALL_XPATH)
        mark_all_radio.click()

    def submit(self):
        check_visible(self._SUBMIT_XPATH, self.driver)
        submit_btn = self.driver.find_element_by_xpath(self._SUBMIT_XPATH)
        submit_btn.click()
        check_invisible(self._SELF_XPATH, self.driver)

    def delete(self):
        check_visible(self._DELETE_XPATH, self.driver)
        del_btn = self.driver.find_element_by_xpath(self._DELETE_XPATH)
        del_btn.click()
        check_visible(self._DEL_YES_XPATH, self.driver)
        del_yes = self.driver.find_element_by_xpath(self._DEL_YES_XPATH)
        del_yes.click()

    def check_has_source_error(self):
        return check_visible(self._SOURCE_ERR_XPATH, self.driver)

class AudienceElement(Component):
    HDR_XPATH_TMPL = '//div[contains(@class, "audience-list-item__name") and text()="%s"]'
    _FORM_XPATH_ADDITION = '/following-sibling::*[contains(@class, "audience-list-item__form")]/div[contains(@class, "audience-form")]'

    def __init__(self, driver, name):
        Component.__init__(self, driver)
        self.name = name
        self.HDR_XPATH = AudienceElement.HDR_XPATH_TMPL % name

    def get_form(self):
        return AudienceForm(self.driver, self.HDR_XPATH + AudienceElement._FORM_XPATH_ADDITION)

    def delete(self):
        hdr = self.driver.find_element_by_xpath(self.HDR_XPATH)
        hdr.click()
        check_visible(self.HDR_XPATH + self._FORM_XPATH_ADDITION, self.driver)
        aud_form = self.get_form()
        aud_form.delete()
        check_invisible(self.HDR_XPATH, self.driver)

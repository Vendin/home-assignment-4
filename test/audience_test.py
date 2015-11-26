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
from page.main_page import MainPage
from test import TargetTest
from page.page import Page, Component
from page.audience_page import AudiencePage, AudienceElement, AudienceForm


class TargetTestAudience(TargetTest):

    def open(self):
        self.page = AudiencePage(self.driver)
        self.page.open()

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

    def test_vk_ctr_filters_wrong(self):
        vk_strange_theme = "asdfsdfsdfsdfasdf12312@as2"
        vk_ctr_adder = self.page.get_vk_group_adder()
        vk_ctr_adder.input_group(vk_strange_theme)
        self.assertFalse(vk_ctr_adder.check_has_helper())

    def test_vk_app_filters_wrong(self):
        vk_strange_app = "asdfsdfsdfsdfasdf12312@as2"
        vk_app_adder = self.page.get_vk_app_adder()
        vk_app_adder.input_group(vk_strange_app)
        self.assertFalse(vk_app_adder.check_has_helper())

    def test_vk_app_has_helper(self):
        vk_app_name = "Mail"
        vk_app_adder = self.page.get_vk_app_adder()
        vk_app_adder.input_group(vk_app_name)
        self.assertTrue(vk_app_adder.check_has_helper())

    def test_page_has_create_aud_btn(self):
        self.assertTrue(self.page.has_create_aud_btn())

    def test_create_aud_filters_empty_source(self):
        aud_name = "My auditory"
        aud_form = self.page.get_create_aud_form()
        aud_form.input_name(aud_name)
        aud_form.submit()
        self.assertTrue(aud_form.check_has_source_error())

    def test_aud_creates(self):
        aud_name = "My auditory"
        aud_form = self.page.get_create_aud_form()
        aud_form.input_name(aud_name)
        aud_form.mark_all()
        aud_form.submit()
        aud_element = self.page.get_aud_element(aud_name)
        self.assertIsNotNone(aud_element)
        aud_element = self.page.get_aud_element(aud_name)
        aud_element.delete()


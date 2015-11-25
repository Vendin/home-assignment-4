import os
import unittest
from selenium import webdriver
from page.main_page import MainPage
from selenium.webdriver import DesiredCapabilities, Remote


class TargetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = os.environ.get('TTHA4BROWSER', 'CHROME')
        cls.password = os.environ.get('TTHA4PASSWORD', 'password')
        cls.login = os.environ.get('TTHA4LOGIN', 'login')
        cls.mode = os.environ.get('TTHA4MODE', 'mail')


    def setUp(self):
        """"
        For webdriver
        if self.browser == 'CHROME': self.driver = webdriver.Chrome()
        else: self.driver = webdriver.Firefox()
        """
        """
        This is for grid
        """
        self.driver = Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, self.browser).copy()
        )

        main_page = MainPage(self.driver)
        main_page.open()
        main_page.login_mail(self.login, self.password)
        self.open();

    def open(self):
        return

    def tearDown(self):
        self.page.close()
        self.driver.quit()

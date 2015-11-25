from page import Page, Component
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MainPage(Page):
    PATH = ''

    HDR_XPATH = '//span[contains(@class, "ph-button__inner_profilemenu_signin")]'
    MENU_BTN_XPATH = '//span[@xname="clb2490734"]'

    INTERNAL_URL = 'https://target.my.com/ads/campaigns/'
    INTERNAL_ELEMENT_XPATH = '//*[contains(@class, "js-nav-link-campaigns")]'

    @property
    def login_button(self):
        return Button(self.driver, self.HDR_XPATH)

    def login_button_exists(self):
        return Page.check_element_exists(self, self.HDR_XPATH)

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
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, self.INTERNAL_ELEMENT_XPATH)
            )
        )

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

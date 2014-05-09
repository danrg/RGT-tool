"""
This file includes the base test class that every test class MUST extend. It handles the set up
and the tear down operations, as well as it provides general functions.

General Functions:
    - can_login
    - wait_for_dialog_box_with_message

"""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from xvfbwrapper import Xvfb
from RGT.settings import RUN_TESTS_IN_BACKGROUND
import time


class BaseLiveTest(LiveServerTestCase):
    @classmethod
    def setUp(self):
        if RUN_TESTS_IN_BACKGROUND:
            self.xvfb = Xvfb(width=1280, height=720)
            self.xvfb.start()
        self.browser = webdriver.Chrome()

    @classmethod
    def tearDown(self):
        self.browser.quit()
        if RUN_TESTS_IN_BACKGROUND:
            self.xvfb.stop()

    # This function performs an implicit test that the user can login. This is used in the base
    # test class, as the login operation is required in the majority of the test cases.
    def can_login(self, email='', password='', login_first_time=True):
        if login_first_time:
            # User opens the web browser and goes to RGT home page
            self.browser.get(self.live_server_url + '/home/')

            # User sees the RGT login page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Login', body.text)

        # User types email and password and hits enter
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys(email)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # email and password are accepted, and the user is redirected to
        # the Home page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Welcome', body.text)

    def wait_for_dialog_box_with_message(self, message=''):
        # wait for the dialog box to appear with the desired message
        WebDriverWait(self.browser, 10).until(
            lambda x: self.browser.find_element_by_css_selector("div[class*='ui-dialog'][style*='block']"))
        dialog_box = self.browser.find_element_by_class_name("ui-dialog")
        self.assertIn(message, dialog_box.text)

        # User clicks the close button to close the dialog
        close_dialog_button = self.browser.find_element_by_css_selector("button[role='button']")
        close_dialog_button.click()

        # Do nothing after the dialog box disappeared
        time.sleep(1)
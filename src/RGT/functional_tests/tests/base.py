"""
This file includes the base test class that every test class MUST extend. It handles the set up
and the tear down operations, as well as it provides general functions.

General Functions:
    - can_login

"""
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class BaseLiveTest(LiveServerTestCase):
    
    @classmethod
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    @classmethod
    def tearDown(self):
        self.browser.quit()
    
    # This function performs an implicit test that the user can login. This is used in the base
    # test class, as the login operation is required in the majority of the test cases.
    def can_login(self, email='', password=''):
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
        
"""
This file is used for the functional tests related to authentication operations,
using the selenium module. These will pass when you run "manage.py test authentication_functional_tests".

Test Classes Used:
    - Register Test

"""
from RGT.base_functional_tests.tests import BaseLiveTest
from selenium.webdriver.common.keys import Keys

class RegisterTest(BaseLiveTest):
    
    def test_can_register(self):
        # # User opens the web browser and goes to RGT home page
        self.browser.get(self.live_server_url + '/home/')
        
        # User sees the RGT login page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Login', body.text)
        
        # User clicks the register link and sees the register page
        register_link = self.browser.find_element_by_id('register-link')
        register_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Register', body.text)
        
        # User types email, first name, last name, password and retype-password
        # and clicks enter. Exception here is that the registration will not be completed
        # due to captcha functionality.
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('test@test.com')
        
        first_name_field = self.browser.find_element_by_name('firstName')
        first_name_field.send_keys('test')
        
        last_name_field = self.browser.find_element_by_name('lastName')
        last_name_field.send_keys('test')
        
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('123')
        
        retype_password_field = self.browser.find_element_by_name('retyped')
        retype_password_field.send_keys('123')
        retype_password_field.send_keys(Keys.RETURN)
        
        # User details accepted and users sees the Home page
        body = self.browser.find_element_by_tag_name('body')
        # self.assertIn('Home', body.text)
        
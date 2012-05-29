"""
This file is used for the functional tests related to session operations,
using the selenium module. These will pass when you run "manage.py test functional_tests.SessionTests".

"""
from RGT.functional_tests.tests.base import BaseLiveTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class BaseSessionLiveTest(BaseLiveTest):
    
    def can_goto_session_page(self):
        # User logs in successfully
        self.can_login()
        
        # User clicks 'Sessions' link and sees the sessions page
        sessions_link = self.browser.find_element_by_link_text("Sessions")
        sessions_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Session administration', body.text)
        
class SessionTests(BaseSessionLiveTest):
    fixtures = ['user_grid_state.json']
    
    def test_can_create_session(self):
        # User logs in successfully and goes to sessions page
        self.can_goto_session_page()
        
        # User clicks the create link and goes to create session page
        create_session_link = self.browser.find_element_by_link_text("create")
        create_session_link.click()
        
        body = self.browser.find_element_by_tag_name("body")
        self.assertIn("Create Session", body.text)
        
        # The 'select' tag contains the created grid with name 'grid1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('grid1', select_field.text)
        
        # User selects the option with grid name 'grid1' and sees the grid with the
        # name 'grid1' in the input text.
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()
        
        # Wait until the the grid appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("gridTrableContainerDiv"))
        
        # User types session name
        session_name_field = self.browser.find_element_by_id("sessionNameInputBox")
        session_name_field.send_keys("session1")
        
        # User clicks the create session button
        create_session_button = self.browser.find_element_by_css_selector("input[value='Create Session']")
        create_session_button.click()
        
        # A dialog box appears with the message 'Grid was created.'
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("div[role='dialog']"))
        dialog_box = self.browser.find_element_by_class_name("ui-dialog")
        self.assertIn('Session was created.', dialog_box.text)
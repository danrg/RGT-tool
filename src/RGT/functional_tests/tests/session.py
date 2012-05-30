"""
This file is used for the functional tests related to session operations,
using the selenium module. These will pass when you run "manage.py test functional_tests.SessionTests".

"""
from RGT.functional_tests.tests.base import BaseLiveTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class BaseSessionLiveTest(BaseLiveTest):
    """
    This is the base class test which the SessionTests class must extend. It defines some
    general functions used by many test cases.
    
    General Functions:
        - can_goto_session_page
    
    """
    
    def can_goto_session_page(self, email='', password=''):
        # User logs in successfully
        self.can_login(email, password)
        
        # User clicks 'Sessions' link and sees the sessions page
        sessions_link = self.browser.find_element_by_link_text("Sessions")
        sessions_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Session administration', body.text)
        
    def facilitator_can_select_session(self, email='', password=''):
        # Facilitator logs in successfully and goes to sessions page
        self.can_goto_session_page(email, password)
        
        # The 'select' tag contains the created session with name 'session1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('session1', select_field.text)
        
        # Facilitator selects the option with session name 'session1' and sees the session with the
        # name 'session1' in the session name row of the session details table.
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()
        
        # Wait until the the session and its details appear successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("sessionDetails"))
        session_details_body = self.browser.find_element_by_id("sessionDetails")
        self.assertIn('session1', session_details_body.text)
        
    def participant_can_select_session(self, email='', password=''):
        # Participant logs in successfully and goes to sessions page
        self.can_goto_session_page(email, password)
        
        # Participant clicks the link to go the the participants page
        participant_page_link = self.browser.find_element_by_link_text("here")
        participant_page_link.click()
        
        # The 'select' tag contains the joined session with name 'admin:session1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('admin:session1', select_field.text)
        
        # Participant selects the option with joined session name 'admin:session1' and sees the session
        # with its details in the sessions details table
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()
        
        # Wait until the the session and its details appear successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_tag_name("table"))
        body = self.browser.find_element_by_tag_name("body")
        self.assertIn("Session details", body.text)
        
class SessionTests(BaseSessionLiveTest):
    """
    This is the base session state that the facilitator and participant session tests extend. It
    provides the needed fixtures.
    
    """
    fixtures = ['user_grid_state.json']
    
class FacilitatorSessionTests(SessionTests):
    
    def test_can_create_session(self):
        # User logs in successfully and goes to sessions page
        self.can_goto_session_page('admin@admin.com', '123')
        
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
        
        # User clicks the close button to close the dialog
        close_dialog_button = self.browser.find_element_by_css_selector("button[role='button']")
        close_dialog_button.click()
    
    def test_can_start_session(self):
        # Facilitator logs in successfully, goes to session page and select a session
        self.facilitator_can_select_session('admin@admin.com', '123')
    
    def test_can_change_session_state(self):
        pass
    
    def test_can_end_session(self):
        pass
    
class ParticipantSessionTests(SessionTests):
    
    def test_join_session(self):
        pass
    
    def test_can_respond_to_request(self):
        # Participant logs in successfully, goes to session page in participating session part
        # and selects a session, he is participating in
        self.participant_can_select_session('test1@test1.com', '123')
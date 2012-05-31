"""
This file is used for the functional tests related to session operations,
using the python selenium module. These will pass when you run:
    
    manage.py test functional_tests.SessionTests
    
This file also includes the base test for the session which includes general functions needed
by the test cases.

"""
from RGT.functional_tests.tests.base import BaseLiveTest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from random import randint

class BaseSessionLiveTest(BaseLiveTest):
    """
    This is the base class test which the SessionTests class must extend. It defines some
    general functions used by the test cases of session process, facilitator and participant.
    The fixtures loaded with this class are used for the test cases of the session process,
    facilitator and participant.
    
    General Functions:
        - can_goto_session_page
        - facilitator_can_select_session
        - participant_can_select_session
    
    """
    fixtures = ['user_grid_state.json']
    
    def can_goto_session_page(self, email='', password='', login_first_time=True):
        # User logs in successfully
        self.can_login(email, password, login_first_time)
        
        # User clicks 'Sessions' link and sees the sessions page
        sessions_link = self.browser.find_element_by_link_text("Sessions")
        sessions_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Session administration', body.text)
        
    def facilitator_can_select_session(self, email='', password='', session_name='', login_first_time=True):
        # Facilitator logs in successfully and goes to sessions page
        self.can_goto_session_page(email, password, login_first_time)
        
        # The 'select' tag contains the created session with name 'session1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn(session_name, select_field.text)
        
        # Facilitator selects the option with session name 'session1' and sees the session with the
        # name 'session1' in the session name row of the session details table.
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()
        
        # Wait until the the session and its details appear successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("sessionDetails"))
        session_details_body = self.browser.find_element_by_id("sessionDetails")
        self.assertIn('session1', session_details_body.text)
        
    def participant_can_select_session(self, email='', password='', session_name='', login_first_time=True):
        # Participant logs in successfully and goes to sessions page
        self.can_goto_session_page(email, password, login_first_time)
        
        # Participant clicks the link to go the the participants page
        participant_page_link = self.browser.find_element_by_link_text("here")
        participant_page_link.click()
        
        # The 'select' tag contains the joined session with name 'admin:session1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn(session_name, select_field.text)
        
        # Participant selects the option with joined session name 'admin:session1' and sees the session
        # with its details in the sessions details table
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()
        
        # Wait until the the session and its details appear successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='Send Response']"))
        body = self.browser.find_element_by_tag_name("body")
        self.assertIn("Session details", body.text)
        
class SessionTests(BaseSessionLiveTest):
    """
    This class...
    
    Test cases implemented:
        - Session Process Test
    
    """ 
    
    def fill_empty_ratings(self, two_grids=False):
        number_of_alternatives = 3
        number_of_concerns = 5
        for i in range(number_of_concerns):
            if i < 3:
                if two_grids:
                    ratings = self.browser.find_elements_by_name("ratio_concer%d_alternative3" % (i + 1))
                    ratings[1].send_keys(randint(1, 5))
                else:
                    self.browser.find_element_by_name("ratio_concer%d_alternative3" % (i + 1)).send_keys(randint(1, 5))
            else:
                for j in range(number_of_alternatives):
                    if two_grids:
                        ratings = self.browser.find_elements_by_name("ratio_concer%d_alternative%d" % ((i + 1), (j + 1)))
                        ratings[1].send_keys(randint(1, 5))
                    else:
                        self.browser.find_element_by_name("ratio_concer%d_alternative%d" % ((i + 1), (j + 1))).send_keys(randint(1, 5))
                    
    
    def test_session_process(self):
        # Facilitator admin logs in and selects the session with name session1
        self.facilitator_can_select_session("admin@admin.com", "123", "session1")
        
        # Participants panel shows two users with names user1 and user2
        participants_in_panel = self.browser.find_elements_by_class_name("respondedRequest")
        self.assertEqual(participants_in_panel[0].text, "user1")
        self.assertEqual(participants_in_panel[1].text, "user2")
        
        # Facilitator admin clicks the start session button
        start_session_button = self.browser.find_element_by_css_selector("input[value='Start Session']")
        start_session_button.click()
        
        # Wait until the menu of the buttons changes to the session handling menu
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='Request Alt/Con']"))
        
        # The iteration label show iteration 1
        iteration_label = self.browser.find_element_by_id("iteration")
        self.assertIn("1", iteration_label.text)
        
        # The iteration status shows 'Check Values'
        current_iteration_status = self.browser.find_element_by_id("currentIterationStatus")
        self.assertIn("Check Values", current_iteration_status.text)
        
        ### REQUEST ALTERNATIVES / CONCERNS STEP ###
        
        # Facilitator admin clicks the request alternatives and concerns button
        request_alternatives_concerns_button = self.browser.find_element_by_css_selector("input[value='Request Alt/Con']")
        request_alternatives_concerns_button.click()
        
        # Wait until the session menu changes, to include the finish session button
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='Finish Request']"))
        
        # The iteration status shows 'A/C'
        current_iteration_status = self.browser.find_element_by_id("currentIterationStatus")
        self.assertIn("A/C", current_iteration_status.text)
        
        # Facilitator admin logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()
        
        ### RESPOND ALTERNATIVES / CONCERN STEP ###
        
        # Participant user1 logs in, goes to participating session
        # page and selects the session session1 of admin
        self.participant_can_select_session("test1@test1.com", "123", "admin:session1", False)
        
        # Participant user1 mouse over to alternative2
        # (because there are two grids, there are also two alternative fields with the same name)
        alternatives_with_name_alternative_2 = self.browser.find_elements_by_name("alternative_2_name")
        ActionChains(self.browser).move_to_element(alternatives_with_name_alternative_2[1]).perform()
        
        # Participant user1 clicks the button to add a column
        add_column_button = self.browser.find_element_by_xpath("//div[@class='colMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_column_button.click()
        
        # Participant user1 types value for alternative3
        alternative_3_name = self.browser.find_element_by_name("alternative_3_name")
        alternative_3_name.send_keys('a3')
        
        # Participant user1 sends the response and logs out
        send_response_button = self.browser.find_element_by_css_selector("input[value='Send Response']")
        send_response_button.click()
        
        self.wait_for_dialog_box_with_message("Response was sent.")
        
        # Participant user1 logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()
        
        # Participant user2 logs in, goes to participating session
        # page and selects the session session1 of user admin
        self.participant_can_select_session("test2@test2.com", "123", "admin:session1", False)
        
        # Participant user2 mouse over concern_3_left
        # (because there are two grids, there are also two concerns with the same name)
        concerns_with_name_concern_3_left = self.browser.find_elements_by_name("concern_3_left")
        ActionChains(self.browser).move_to_element(concerns_with_name_concern_3_left[1]).perform()
        
        # Participant user2 clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()
        
        # Participant user2 types left and right value for concern4
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        concern_4_left.send_keys('l4')
        concern_4_right = self.browser.find_element_by_name("concern_4_right")
        concern_4_right.send_keys('r4')
        
        # Participant user2 mouse over concern_4_left
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        ActionChains(self.browser).move_to_element(concern_4_left).perform()
        
        # Participant user2 clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()
        
        # Participant user2 types left and right value for concern5
        concern_5_left = self.browser.find_element_by_name("concern_5_left")
        concern_5_left.send_keys('l5')
        concern_5_right = self.browser.find_element_by_name("concern_5_right")
        concern_5_right.send_keys('r5')
        
        # Participant user2 sends the response
        send_response_button = self.browser.find_element_by_css_selector("input[value='Send Response']")
        send_response_button.click()
        
        self.wait_for_dialog_box_with_message("Response was sent.")
        
        # Participant user2 logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()
        
        ### REQUEST RATINGS STEP ###
        
        # Facilitator admin logs in, selects the session with name session1
        self.facilitator_can_select_session("admin@admin.com", "123", "session1")
        
        # Facilitator admin clicks the finish request button
        finish_request_button = self.browser.find_element_by_css_selector("input[value='Finish Request']")
        finish_request_button.click()
        
        # Wait until the session menu changes, to include the request ratings button
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='Request Ratings']"))
        
        # The iteration label show iteration 2
        iteration_label = self.browser.find_element_by_id("iteration")
        self.assertIn("2", iteration_label.text)
        
        # The iteration status shows 'Check Values'
        current_iteration_status = self.browser.find_element_by_id("currentIterationStatus")
        self.assertIn("Check Values", current_iteration_status.text)
        
        # Facilitator admin selects from the select field the results from iteration 1
        show_respond_from_iterations_options = self.browser.find_elements_by_xpath("//select[@id='mySessionsContentSessionIterationSelect']/option")
        show_respond_from_iterations_options[1].click()
        
        # Wait until the results from the selected iteration appear
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("resultAlternativeConcernTablesDiv"))
        
        # Facilitator admin updates the grid with the new values from the participants
        # Facilitator admin mouse over to alternative2
        alternative_2_name = self.browser.find_element_by_name("alternative_2_name")
        ActionChains(self.browser).move_to_element(alternative_2_name).perform()
        
        # Facilitator admin clicks the button to add a column
        add_column_button = self.browser.find_element_by_xpath("//div[@class='colMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_column_button.click()
        
        # Facilitator admin types value for alternative3
        alternative_3_name = self.browser.find_element_by_name("alternative_3_name")
        alternative_3_name.send_keys('a3')
        
        concern_3_left = self.browser.find_element_by_name("concern_3_left")
        ActionChains(self.browser).move_to_element(concern_3_left).perform()
        
        # Facilitator admin clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()
        
        # Facilitator admin types left and right value for concern4
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        concern_4_left.send_keys('l4')
        concern_4_right = self.browser.find_element_by_name("concern_4_right")
        concern_4_right.send_keys('r4')
        
        # Facilitator admin mouse over concern_4_left
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        ActionChains(self.browser).move_to_element(concern_4_left).perform()
        
        # Facilitator admin clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()
        
        # Facilitator admin types left and right value for concern5
        concern_5_left = self.browser.find_element_by_name("concern_5_left")
        concern_5_left.send_keys('l5')
        concern_5_right = self.browser.find_element_by_name("concern_5_right")
        concern_5_right.send_keys('r5')
        
        # Facilitator admin saves the new grid
        save_changes_button = self.browser.find_element_by_css_selector("input[value='Save Changes']")
        save_changes_button.click()
        
        # A dialog box appears with the message 'Grid was saved'
        self.wait_for_dialog_box_with_message("Grid was saved")
        
        # Facilitator admin clicks the clear results button to clear the results
        clear_results_button = self.browser.find_element_by_css_selector("input[value='Clear Results']")
        clear_results_button.click()
        
        # Wait until the results are cleared
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("mySessionsContentResultDiv").text == "")
        
        # Facilitator admin clicks the request ratings button
        request_ratings_button = self.browser.find_element_by_css_selector("input[value='Request Ratings']")
        request_ratings_button.click()
        
        # Wait until the session menu changes, to include the finish session button
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='Finish Request']"))
        
        # The iteration status shows 'R/W'
        current_iteration_status = self.browser.find_element_by_id("currentIterationStatus")
        self.assertIn("R/W", current_iteration_status.text)
        
        # Facilitator admin logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()
        
        ### RESPOND RATINGS STEP ###
        
        # Participant with the name user1 logs in, goes to participating session
        # page and selects the session session1 of user admin
        self.participant_can_select_session("test1@test1.com", "123", "admin:session1", False)
        
        # Participant user1 types some values for the ratings
        self.fill_empty_ratings(True)
        
        # Participant user1 sends the response
        send_response_button = self.browser.find_element_by_css_selector("input[value='Send Response']")
        send_response_button.click()
        
        self.wait_for_dialog_box_with_message("Response was sent.")
        
        # Participant user1 logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()
        
        # Participant with the name user2 logs in, goes to participating session
        # page and selects the session session1 of user admin
        self.participant_can_select_session("test2@test2.com", "123", "admin:session1", False)
        
        # Participant user2 types some values for the ratings
        self.fill_empty_ratings(True)
        
        # Participant user2 sends the response
        send_response_button = self.browser.find_element_by_css_selector("input[value='Send Response']")
        send_response_button.click()
        
        self.wait_for_dialog_box_with_message("Response was sent.")
        
        # Participant user2 logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()
        
        ### END SESSION STEP ###
        
        # Facilitator admin logs in, selects the session with name session1
        self.facilitator_can_select_session("admin@admin.com", "123", "session1")
        
        # Facilitator admin clicks the finish request button
        finish_request_button = self.browser.find_element_by_css_selector("input[value='Finish Request']")
        finish_request_button.click()
        
        # Wait until the session menu changes, to include the request ratings button
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='End Session']"))
        
        # The iteration label show iteration 2
        iteration_label = self.browser.find_element_by_id("iteration")
        self.assertIn("3", iteration_label.text)
        
        # The iteration status shows 'Check Values'
        current_iteration_status = self.browser.find_element_by_id("currentIterationStatus")
        self.assertIn("Check Values", current_iteration_status.text)
        
        # Facilitator admin selects from the select field the results from iteration 2
        show_respond_from_iterations_options = self.browser.find_elements_by_xpath("//select[@id='mySessionsContentSessionIterationSelect']/option")
        show_respond_from_iterations_options[2].click()
        
        # Wait until the results from the selected iteration appear
        self.wait_for_dialog_box_with_message("The dendrogram of iteration 2 cannot be generated. Ratings must be complete in order to generate a dendrogram.")
        
        # Facilitator admin type some values for the ratings
        self.fill_empty_ratings()
        
        # Facilitator admin saves the changes
        save_changes_button = self.browser.find_element_by_css_selector("input[value='Save Changes']")
        save_changes_button.click()
        
        # A dialog box appears with the message 'Grid was saved'
        self.wait_for_dialog_box_with_message("Grid was saved")
        
        # Facilitator clicks the show dendrogram button and gets the dendrogram
        show_dendrogram_button = self.browser.find_element_by_css_selector("input[value='Show Dendrogram']")
        show_dendrogram_button.click()
        
        # Wait until the dendrogram appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_class_name("hasSVG"))
        
        end_session_button = self.browser.find_element_by_css_selector("input[value='End Session']")
        end_session_button.click()
        
        # Wait until the status change to Closed
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("currentIterationStatus").text == "Closed")
    
class FacilitatorSessionTests(BaseSessionLiveTest):
    """
    This class...
    
    Test cases implemented:
        - Create Session Test
    
    """
    
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
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_class_name("gridTrableContainerDiv"))
        
        # User types session name
        session_name_field = self.browser.find_element_by_id("sessionNameInputBox")
        session_name_field.send_keys("session3")
        
        # User clicks the create session button
        create_session_button = self.browser.find_element_by_css_selector("input[value='Create Session']")
        create_session_button.click()
        
        # A dialog box appears with the message 'Session was created.'
        self.wait_for_dialog_box_with_message("Session was created.")
    
class ParticipantSessionTests(BaseSessionLiveTest):
    """
    This class...
    
    Test cases implemented:
        - Join Session Test
    
    """
    
    def test_join_session(self):
        # Participator logs in successfully, goes to participating session page
        self.can_goto_session_page("test1@test1.com", "123")
        
        # Participant clicks the link to go the the participants page
        participant_page_link = self.browser.find_element_by_link_text("here")
        participant_page_link.click()
        
        # Participant types the invitation key on the field and clicks the join button
        invitation_key_field = self.browser.find_element_by_id("invitationKeyInput")
        invitation_key_field.send_keys("1dec5aaa-1c53-43bf-9d71-f5cf56ca50c9")
        
        join_session_button = self.browser.find_element_by_css_selector("input[value='Join Session']")
        join_session_button.click()
        
        # Wait for a success message to appear in dialog box
        self.wait_for_dialog_box_with_message('You have been added as participant in session: "session2".')
        
        # The participating session with name admin:session2 appears in the select tag
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('admin:session2', select_field.text)
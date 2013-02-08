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
import time

class BaseSessionLiveTest(BaseLiveTest):
    """
    This is the base class test which the rest session related test classes must extend.
    It defines some general functions used by the test cases of session process, facilitator
    and participant. The fixtures loaded with this class are used for the test cases of the
    session process, facilitator and participant.
    
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

        # The 'select' tag contains the created session with the name session_name
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn(session_name, select_field.text)

        # Facilitator selects the option with session name session_name and sees the session with the
        # name session_name in the session name row of the session details table.
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

        # The 'select' tag contains the joined session with name session_name
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn(session_name, select_field.text)

        # Participant selects the option with joined session name session_name and sees the session
        # with its details in the sessions details table
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()

        # Wait until the the session and its details appear successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("sessionDetails"))
        body = self.browser.find_element_by_tag_name("body")
        self.assertIn("Session details", body.text)

class SessionTests(BaseSessionLiveTest):
    """
    This class includes tests related to the session process.
    
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

        #Process to create a session with name session3
        #user logs in successfully and sees the sessions page
        self.can_goto_session_page("admin@admin.com", "123")

        # User clicks the create session link and sees the create session page
        create_session_link = self.browser.find_element_by_link_text("create")
        create_session_link.click()

        # user selects grid to create the session
        select_grid_field = self.browser.find_element_by_css_selector("select[id='gridSessionSelection']")
        self.assertIn('grid1', select_grid_field.text)

        # User selects the option with grid name 'grid1' and sees the grid with the
        # name 'grid1' in the input text.
        option_grid_fields = self.browser.find_elements_by_css_selector('option')
        option_grid_fields[1].click()

        # user enters the session name
        session_new_name = self.browser.find_element_by_id("sessionNameInputBox")
        session_new_name.send_keys('session3')

        # user checks the radio button to allow the participants to see the results
        show_results = self.browser.find_element_by_css_selector("input[value='Y']")
        show_results.click()

        # user creates session
        create_button = self.browser.find_element_by_css_selector("input[value='Create Session']")
        create_button.click()

        # A dialog box appears with the message 'Session was created.' and user closes it
        self.wait_for_dialog_box_with_message("Session was created.")

        # user logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

        # Facilitator admin logs in and selects the session with name session1
        self.facilitator_can_select_session("admin@admin.com", "123", "session1")

        # Participants panel shows two users with names user1 and user2
        participants_in_panel = self.browser.find_elements_by_class_name("respondedRequest")
        self.assertEqual(participants_in_panel[0].text, "test1")
        self.assertEqual(participants_in_panel[1].text, "test2")

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

        # The number of participants shows 0/2 which means that none participant responded yet
        session_details_body = self.browser.find_element_by_id("sessionDetails")
        self.assertIn("0/2", session_details_body.text)

        # Participant user1 mouse over to alternative_2
        # (because there are two grids, there are also two alternative fields with the same name)
        alternatives_with_name_alternative_2 = self.browser.find_elements_by_name("alternative_2_name")
        ActionChains(self.browser).move_to_element(alternatives_with_name_alternative_2[1]).perform()

        # Participant user1 clicks the button to add a column
        add_column_button = self.browser.find_element_by_xpath("//div[@class='colMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_column_button.click()

        # Participant user1 types value for alternative_3
        alternative_3_name = self.browser.find_element_by_name("alternative_3_name")
        alternative_3_name.send_keys('a3')

        # Participant user1 sends the response and logs out
        send_response_button = self.browser.find_element_by_css_selector("input[value='Send Response']")
        send_response_button.click()

        self.wait_for_dialog_box_with_message("Response was sent.")

        # Refresh the page after response was sent
        refresh_button = self.browser.find_element_by_id("participatingSessionsRefreshImage")
        refresh_button.click()

        time.sleep(10)

        # The number of participants shows 1/2 which means that one out of 2 participants responded
        # and the response status says Response was sent
        session_details_body = self.browser.find_element_by_id("sessionDetails")
        self.assertIn("1/2", session_details_body.text)
        self.assertIn("Response was sent at:", session_details_body.text)

        # Participant user1 logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

        # Participant user2 logs in, goes to participating session
        # page and selects the session session1 of user admin
        self.participant_can_select_session("test2@test2.com", "123", "admin:session1", False)

        # The number of participants shows 1/2 which means that one out of 2 participants responded
        session_details_body = self.browser.find_element_by_id("sessionDetails")
        self.assertIn("1/2", session_details_body.text)

        # Participant user2 mouse over concern_3_left
        # (because there are two grids, there are also two concerns with the same name)
        concerns_with_name_concern_3_left = self.browser.find_elements_by_name("concern_3_left")
        ActionChains(self.browser).move_to_element(concerns_with_name_concern_3_left[1]).perform()

        # Participant user2 clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()

        # Participant user2 types left and right value for concern_4
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        concern_4_left.send_keys('l04')
        concern_4_right = self.browser.find_element_by_name("concern_4_right")
        concern_4_right.send_keys('r04')

        # Participant user2 mouse over concern_4_left
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        ActionChains(self.browser).move_to_element(concern_4_left).perform()

        # Participant user2 clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()

        # Participant user2 types left and right value for concern_5
        concern_5_left = self.browser.find_element_by_name("concern_5_left")
        concern_5_left.send_keys('l05')
        concern_5_right = self.browser.find_element_by_name("concern_5_right")
        concern_5_right.send_keys('r05')

        # Participant user2 sends the response
        send_response_button = self.browser.find_element_by_css_selector("input[value='Send Response']")
        send_response_button.click()

        self.wait_for_dialog_box_with_message("Response was sent.")

        # Refresh the page after response was sent
        refresh_button = self.browser.find_element_by_id("participatingSessionsRefreshImage")
        refresh_button.click()

        time.sleep(10)

        # The number of participants shows 2/2 which means that all participants responded
        # and the response status says Response was sent
        session_details_body = self.browser.find_element_by_id("sessionDetails")
        self.assertIn("2/2", session_details_body.text)
        self.assertIn("Response was sent at:", session_details_body.text)

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

        # The iteration label shows iteration 2
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

        # Facilitator admin clicks the button to download results
        download_result1_button = self.browser.find_element_by_id("downloadResultsButton")
        download_result1_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("select[name='convertTo']"))

        # User types value for filename
        grid_file_name = self.browser.find_element_by_name("fileName")
        grid_file_name.send_keys('resultsIteration1')

        #for future use
        #download_button = self.browser.find_element_by_css_selector("button[class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
        #download_button.click()

        close_button = self.browser.find_element_by_css_selector("a[class='ui-dialog-titlebar-close ui-corner-all']")
        close_button.click()

        # Facilitator admin mouse over to alternative_2
        alternative_2_name = self.browser.find_element_by_name("alternative_2_name")
        ActionChains(self.browser).move_to_element(alternative_2_name).perform()

        # Facilitator admin clicks the button to add a column
        add_column_button = self.browser.find_element_by_xpath("//div[@class='colMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_column_button.click()

        # Facilitator admin types value for alternative_3
        alternative_3_name = self.browser.find_element_by_name("alternative_3_name")
        alternative_3_name.send_keys('a3')

        # Facilitator admin mouse over to concern_3_left
        concern_3_left = self.browser.find_element_by_name("concern_3_left")
        ActionChains(self.browser).move_to_element(concern_3_left).perform()

        # Facilitator admin clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()

        # Facilitator admin types left and right value for concern_4
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        concern_4_left.send_keys('l04')
        concern_4_right = self.browser.find_element_by_name("concern_4_right")
        concern_4_right.send_keys('r04')

        # Facilitator admin mouse over concern_4_left
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        ActionChains(self.browser).move_to_element(concern_4_left).perform()

        # Facilitator admin clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()

        # Facilitator admin types left and right value for concern5
        concern_5_left = self.browser.find_element_by_name("concern_5_left")
        concern_5_left.send_keys('l05')
        concern_5_right = self.browser.find_element_by_name("concern_5_right")
        concern_5_right.send_keys('r05')

        self.fill_empty_ratings(False)

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

        # Facilitator clicks the show dendrogram button and gets the dendrogram
        show_dendrogram_button = self.browser.find_element_by_css_selector("input[value='Show Dendrogram']")
        show_dendrogram_button.click()

        time.sleep(10)

        # Wait until the dendrogram appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_class_name("dendrogramTitle"))

        # Facilitator admin logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

        ### RESPOND RATINGS STEP ###

        # Participant with the name user1 logs in, goes to participating session
        # page and selects the session session1 of user admin
        self.participant_can_select_session("test1@test1.com", "123", "admin:session1", False)

        # Participant user1 types some values for the ratings
        #self.fill_empty_ratings(True)

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
        #self.fill_empty_ratings(True)

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

        # Wait until the session menu changes, to include the end session button
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("input[value='End Session']"))

        # The iteration label shows iteration 2
        iteration_label = self.browser.find_element_by_id("iteration")
        self.assertIn("3", iteration_label.text)

        # The iteration status shows 'Check Values'
        current_iteration_status = self.browser.find_element_by_id("currentIterationStatus")
        self.assertIn("Check Values", current_iteration_status.text)

        # Facilitator admin selects from the select field the results from iteration 2
        show_respond_from_iterations_options = self.browser.find_elements_by_xpath("//select[@id='mySessionsContentSessionIterationSelect']/option")
        show_respond_from_iterations_options[2].click()

        # Wait until the results from the selected iteration appear
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("clearResultsButton"))

        # User mouse over dendrogram
        results_image = self.browser.find_element_by_id("downloadResultsButton")
        ActionChains(self.browser).move_to_element(results_image).perform()

        time.sleep(2)

        # Facilitator admin clicks the button to download results
        download_result2_button = self.browser.find_element_by_css_selector("input[id='downloadResultsButton']")
        download_result2_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("select[name='convertTo']"))

        # User types value for filename
        grid_file_name = self.browser.find_element_by_name("fileName")
        grid_file_name.send_keys('resultsIteration2')

        #for future use
        #download_button = self.browser.find_element_by_css_selector("button[class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
        #download_button.click()

        close_button = self.browser.find_element_by_css_selector("a[class='ui-dialog-titlebar-close ui-corner-all']")
        close_button.click()


        # Facilitator admin saves the changes
        save_changes_button = self.browser.find_element_by_css_selector("input[value='Save Changes']")
        save_changes_button.click()

        # A dialog box appears with the message 'Grid was saved'
        self.wait_for_dialog_box_with_message("Grid was saved")

        # Facilitator clicks the show dendrogram button and gets the dendrogram
        show_dendrogram_button = self.browser.find_element_by_css_selector("input[value='Show Dendrogram']")
        show_dendrogram_button.click()

        # Wait until the dendrogram appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_tag_name("svg"))

        time.sleep(1)

        # Facilitator admin clicks the end session button
        end_session_button = self.browser.find_element_by_css_selector("input[value='End Session']")
        end_session_button.click()

        # Wait until the status change to Closed
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("currentIterationStatus").text == "Closed")

        time.sleep(1)

        # Facilitator admin logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

        # Facilitator admin logs in, selects the session with name session1
        self.facilitator_can_select_session("admin@admin.com", "123", "session1")

        # Facilitator clicks the show dendrogram button and gets the dendrogram
        show_dendrogram_button = self.browser.find_element_by_css_selector("input[value='Show Dendrogram']")
        show_dendrogram_button.click()

        # Wait until the dendrogram appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_tag_name("svg"))

        time.sleep(1)

        # Facilitator mouse over dendrogram
        dendrogram_image = self.browser.find_element_by_tag_name("svg")
        ActionChains(self.browser).move_to_element(dendrogram_image).perform()

        save_image_button = self.browser.find_element_by_css_selector("img[id='saveButtonImg']")
        save_image_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("select[name='convertTo']"))

        # Facilitator types value for filename
        session_file_name = self.browser.find_element_by_name("fileName")
        session_file_name.send_keys('dendrogram')

        #for future use
        #download_button = self.browser.find_element_by_css_selector("button[class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
        #download_button.click()

        close_button = self.browser.find_element_by_css_selector("a[class='ui-dialog-titlebar-close ui-corner-all']")
        close_button.click()

        # Facilitator admin logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

        # Participant with the name user1 logs in, goes to participating session
        # page and selects the session session1 of user admin
        self.participant_can_select_session("test1@test1.com", "123", "admin:session1", False)

        show_participant_respond_from_iterations_options = self.browser.find_elements_by_xpath("//select[@id='responseSelection']/option")
        show_participant_respond_from_iterations_options[2].click()

        # Wait until the response from the selected iteration appear
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("participationSessionsContentGridsDiv"))

        show_participant_result_from_iterations_options = self.browser.find_elements_by_xpath("//select[@id='resultSelection']/option")
        show_participant_result_from_iterations_options[2].click()

        # Wait until the results from the selected iteration appear
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("clearResultsButton"))

        time.sleep(2)

        # user logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

        # Facilitator admin logs in, selects the session with name session1
        self.facilitator_can_select_session("admin@admin.com", "123", "session1")

        # Facilitator clicks the button to save the grid
        concern_1_left = self.browser.find_element_by_name("concern_1_left")
        ActionChains(self.browser).move_to_element(concern_1_left).perform()
        save_grid_button = self.browser.find_element_by_css_selector("img[title='download grid as']")
        save_grid_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("select[name='convertTo']"))

        # User types value for filename
        grid_file_name = self.browser.find_element_by_name("fileName")
        grid_file_name.send_keys('sessionGrid')

        #for future use
        #download_button = self.browser.find_element_by_css_selector("button[class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
        #download_button.click()

        close_button = self.browser.find_element_by_css_selector("a[class='ui-dialog-titlebar-close ui-corner-all']")
        close_button.click()

        # Facilitator admin logs out
        logout_link = self.browser.find_element_by_link_text("Log out")
        logout_link.click()

class FacilitatorSessionTests(BaseSessionLiveTest):
    """
    This class includes tests related to facilitator operations.
    
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

        # user checks the radio button to allow the participants to see the results
        show_results = self.browser.find_element_by_css_selector("input[value='N']")
        show_results.click()

        # User clicks the create session button
        create_session_button = self.browser.find_element_by_css_selector("input[value='Create Session']")
        create_session_button.click()

        # A dialog box appears with the message 'Session was created.'
        self.wait_for_dialog_box_with_message("Session was created.")

class ParticipantSessionTests(BaseSessionLiveTest):
    """
    This class includes tests related to participant operations.
    
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
        invitation_key_field.send_keys("447d3e47-9706-4239-85fc-614d702bcc3b")

        join_session_button = self.browser.find_element_by_css_selector("input[value='Join Session']")
        join_session_button.click()

        # Wait for a success message to appear in dialog box
        self.wait_for_dialog_box_with_message('You have been added as participant in session: "session2".')

        # The participating session with name admin:session2 appears in the select tag
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('admin:session2', select_field.text)

        time.sleep(1)

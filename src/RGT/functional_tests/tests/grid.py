"""
This file is used for the functional tests related to grid operations,
using the python selenium module. These will pass when you run:

    manage.py test functional_tests.GridTests

This file also includes the base test for the grids which includes general functions needed
by the test cases.

"""
from RGT.functional_tests.tests.base import BaseLiveTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from random import randint
import time

class BaseGridLiveTest(BaseLiveTest):
    """
    This is the base class test which the GridTests class must extend. It defines some
    general functions used by many test cases.
    
    General Functions:
        - can_goto_grid_page
        - can_show_grid
        
    """
    def can_goto_grid_page(self, email='', password=''):
        # User logs in successfully
        self.can_login(email, password)

        # User clicks 'Grids' link and sees the grids page
        grids_link = self.browser.find_element_by_link_text("Grids")
        grids_link.click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Grid Management', body.text)

    def can_select_grid(self, email='', password=''):
        # User logs in successfully and goes to grid page 
        self.can_goto_grid_page(email, password)

        # The 'select' tag contains the created grid with name 'grid1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('grid1', select_field.text)

        # User selects the option with grid name 'grid1' and sees the grid with the
        # name 'grid1' in the input text.
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()

        # Wait until the the grid appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_class_name("gridTrableContainerDiv"))
        grid_name_field = self.browser.find_element_by_name("gridName")
        self.assertEquals('grid1', grid_name_field.get_attribute('value'))

class GridTests(BaseGridLiveTest):
    """
    This class includes the tests related to grid operations.
    
    Test cases implemented:
        - Create Grid Test
        - Update Grid Test
        - Delete Grid Test
        - Show Dendrogram Test
    
    """
    fixtures = ['user_grid.json']

    def test_can_create_grid(self):
        # User logs in successfully and goes to grid page
        self.can_goto_grid_page('admin@admin.com', '123')

        # User clicks the create grid link and sees the create grid page
        create_grid_link = self.browser.find_element_by_link_text("in place")
        create_grid_link.click()

        # new body here because the user redirected to a different page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Create Grid', body.text)

        # User types grid name
        grid_name_field = self.browser.find_element_by_name("gridName")
        grid_name_field.send_keys('grid1')

        # User types two alternatives for the grid
        number_of_alternatives = 2
        for i in range(number_of_alternatives):
            self.browser.find_element_by_name("alternative_%d_name" % (i + 1)).send_keys('a%d' % (i + 1))

        # User types the left and right part of three concerns on the grid
        number_of_concerns = 3
        for i in range(number_of_concerns):
            self.browser.find_element_by_name("concern_%d_left" % (i + 1)).send_keys('l%d' % (i + 1))
            self.browser.find_element_by_name("concern_%d_right" % (i + 1)).send_keys('r%d' % (i + 1))

        # User types six ratings and three weights on the grid
        for i in range(number_of_concerns):
            for j in range(number_of_alternatives):
                rating = self.browser.find_element_by_name("ratio_concer%d_alternative%d" % ((i + 1), (j + 1)))
                rating.send_keys(randint(1, 5))
                rating.send_keys(Keys.TAB)
            weight = self.browser.find_element_by_name("weight_concern%d" % (i + 1))
            weight.send_keys(Keys.CLEAR)
            weight.send_keys(randint(1, 5))

        # User mouser over to concern_1
        concern_1_left = self.browser.find_element_by_name("concern_1_left")
        ActionChains(self.browser).move_to_element(concern_1_left).perform()

        # User clicks the button to hide the legend
        hide_legend_button = self.browser.find_element_by_class_name('gridTableToggleLegendImg')
        hide_legend_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_xpath('//div[@class="tableLegendDiv" and contains(@style, "none")]'))

        # User clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        # A dialog box appears with the message 'Grid was created.' and user closes it
        self.wait_for_dialog_box_with_message("Grid was created.")

    def test_can_download_grid(self):
        # User logs in successfully, goes to grid page and selects a saved grid
        self.can_select_grid('admin@admin.com', '123')

        # User clicks the button to save
        concern_1_left = self.browser.find_element_by_name("concern_1_left")
        ActionChains(self.browser).move_to_element(concern_1_left).perform()
        save_grid_button = self.browser.find_element_by_css_selector("img[title='download grid as']")
        save_grid_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("select[name='convertTo']"))

        # User types value for filename
        grid_file_name = self.browser.find_element_by_name("fileName")
        grid_file_name.send_keys('grid1')


    def test_can_update_grid(self):
        # User logs in successfully, goes to grid page and selects a saved grid
        self.can_select_grid('admin@admin.com', '123')

        # User changes the name of the grid to 'grid123'
        grid_name_field = self.browser.find_element_by_name("gridName")
        grid_name_field.send_keys('23')

        # User mouser over to alternative2
        alternative_2_name = self.browser.find_element_by_name("alternative_2_name")
        ActionChains(self.browser).move_to_element(alternative_2_name).perform()

        # User clicks the button to add a column
        add_column_button = self.browser.find_element_by_xpath("//div[@class='colMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_column_button.click()

        # User types value for alternative3
        alternative_3_name = self.browser.find_element_by_name("alternative_3_name")
        alternative_3_name.send_keys('a3')

        # User types values for the ratings generated by adding a new column
        number_of_concerns = 3
        for i in range(number_of_concerns):
            self.browser.find_element_by_name("ratio_concer%d_alternative3" % (i + 1)).send_keys(randint(1, 5))

        # User mouse over concern_3_left
        concern_3_left = self.browser.find_element_by_name("concern_3_left")
        ActionChains(self.browser).move_to_element(concern_3_left).perform()

        # User clicks the button to add a row
        add_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu leftRowMenuDiv' and contains(@style, 'block')]/a[2]/img[@class='addImage']")
        add_row_button.click()

        # User types left and right value for concern4
        concern_4_left = self.browser.find_element_by_name("concern_4_left")
        concern_4_left.send_keys('l4')
        concern_4_right = self.browser.find_element_by_name("concern_4_right")
        concern_4_right.send_keys('r4')

        # User types values for the ratings generated by adding a new row
        number_of_alternatives = 3
        for i in range(number_of_alternatives):
            self.browser.find_element_by_name("ratio_concer4_alternative%d" % (i + 1)).send_keys(randint(1, 5))

        # Hide legend test here

        # User mouse over to concern_2_right
        concern_2_right = self.browser.find_element_by_name("concern_2_right")
        ActionChains(self.browser).move_to_element(concern_2_right).perform()

        # User clicks the button to delete the second row
        delete_row_button = self.browser.find_element_by_xpath("//div[@class='gridRowMenu rightRowMenuDiv' and contains(@style, 'block')]/a[1]/img[@class='deleteImage']")
        delete_row_button.click()

        # User mouse over to alternative_1_name.
        alternative_1_name = self.browser.find_element_by_name("alternative_1_name")
        ActionChains(self.browser).move_to_element(alternative_1_name).perform()

        # User clicks the button to delete the first column
        delete_column_button = self.browser.find_element_by_xpath("//div[@class='colMenuDiv' and contains(@style, 'block')]/a[1]/img[@class='deleteImage']")
        delete_column_button.click()

        # User clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        # A dialog box appears with the message 'Grid was saved'
        self.wait_for_dialog_box_with_message("Grid was saved")

    def test_can_delete_grid(self):
        # User logs in successfully, goes to grid page and selects a saved grid
        self.can_select_grid('admin@admin.com', '123')

        # User clicks the delete grid button
        delete_button = self.browser.find_element_by_css_selector("input[value='Delete']")
        delete_button.click()

        # A dialog box appears that asks from the user to confirm delete
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("div[role='dialog']"))
        dialog_box = self.browser.find_element_by_class_name("ui-dialog")
        self.assertIn('Delete grid?', dialog_box.text)

        # The user clicks the delete grid button from the dialog box
        delete_grid_button = self.browser.find_element_by_class_name("ui-button-text")
        delete_grid_button.click()

        # A dialog box appears with the message 'Grid was deleted'
        self.wait_for_dialog_box_with_message("Grid was deleted")

    def test_can_show_dendrogram(self):
        # User logs in successfully, goes to grid page and selects a saved grid
        self.can_select_grid('admin@admin.com', '123')

        # User clicks the show dendrogram button
        show_dendrogram_button = self.browser.find_element_by_css_selector("input[value='Show Dendrogram']")
        show_dendrogram_button.click()

        # Wait until the dendrogram appears successfully
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_tag_name("svg"))

        time.sleep(1)

        # User mouse over dendrogram
        dendrogram_image = self.browser.find_element_by_tag_name("svg")
        ActionChains(self.browser).move_to_element(dendrogram_image).perform()

        save_image_button = self.browser.find_element_by_css_selector("img[id='saveButtonImg']")
        save_image_button.click()

        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("select[name='convertTo']"))

        # User types value for filename
        grid_file_name = self.browser.find_element_by_name("fileName")
        grid_file_name.send_keys('image')

"""
This file is used for the functional tests related to grid operations,
using the selenium module. These will pass when you run "manage.py test grid_functional_tests".

Test cases implemented:
    - Create Grid Test
    - Update Grid Test

"""
from RGT.base_functional_tests.tests import BaseLiveTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.selenium import selenium
        
class CreateGridTest(BaseLiveTest):
    fixtures = ['admin_user.json']
        
    def test_can_create_grid(self):
        BaseLiveTest.can_login(self)
        
        # User clicks 'Grids' link and sees the my grids page
        grids_link = self.browser.find_element_by_link_text("Grids")
        grids_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Grid Management', body.text)
        
        # User clicks the create grid link and sees the create grid page
        create_grid_link = self.browser.find_element_by_link_text("create")
        create_grid_link.click()
        
        # new body here because the user redirected to a different page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Create Grid', body.text)
        
        # User types grid name
        grid_name_field = self.browser.find_element_by_name("gridName")
        grid_name_field.send_keys('test grid 1')
        
        # User types two alternatives for the grid
        alternative_1_name = self.browser.find_element_by_name("alternative_1_name")
        alternative_1_name.send_keys('a1')
        alternative_2_name = self.browser.find_element_by_name("alternative_2_name")
        alternative_2_name.send_keys('a2')
        
        # User types the left and right part of three concerns on the grid
        concern_1_left = self.browser.find_element_by_name("concern_1_left")
        concern_1_left.send_keys('l1')
        concern_1_right = self.browser.find_element_by_name("concern_1_right")
        concern_1_right.send_keys('r1')
        concern_2_left = self.browser.find_element_by_name("concern_2_left")
        concern_2_left.send_keys('l2')
        concern_2_right = self.browser.find_element_by_name("concern_2_right")
        concern_2_right.send_keys('r2')
        concern_3_left = self.browser.find_element_by_name("concern_3_left")
        concern_3_left.send_keys('l3')
        concern_3_right = self.browser.find_element_by_name("concern_3_right")
        concern_3_right.send_keys('r3')
        
        # User types six ratings and three weights on the grid
        ratio_concern1_alternative1 = self.browser.find_element_by_name("ratio_concer1_alternative1")
        ratio_concern1_alternative1.send_keys('3')
        ratio_concern1_alternative2 = self.browser.find_element_by_name("ratio_concer1_alternative2")
        ratio_concern1_alternative2.send_keys('3')
        ratio_concern1_alternative2.send_keys(Keys.TAB)
        weight_concern1 = self.browser.find_element_by_name("weight_concern1")
        weight_concern1.send_keys(Keys.CLEAR)
        weight_concern1.send_keys('0.5')
        ratio_concern2_alternative1 = self.browser.find_element_by_name("ratio_concer2_alternative1")
        ratio_concern2_alternative1.send_keys('3')
        ratio_concern2_alternative2 = self.browser.find_element_by_name("ratio_concer2_alternative2")
        ratio_concern2_alternative2.send_keys('3')
        ratio_concern2_alternative2.send_keys(Keys.TAB)
        weight_concern2 = self.browser.find_element_by_name("weight_concern2")
        weight_concern2.send_keys(Keys.CLEAR)
        weight_concern2.send_keys('0.7')
        ratio_concern3_alternative1 = self.browser.find_element_by_name("ratio_concer3_alternative1")
        ratio_concern3_alternative1.send_keys('3')
        ratio_concern3_alternative2 = self.browser.find_element_by_name("ratio_concer3_alternative2")
        ratio_concern3_alternative2.send_keys('3')
        ratio_concern3_alternative2.send_keys(Keys.TAB)
        weight_concern3 = self.browser.find_element_by_name("weight_concern3")
        weight_concern3.send_keys(Keys.CLEAR)
        weight_concern3.send_keys('1.8')
        
        # User clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()
        
        # A dialog box appears with the message 'Grid was created.'
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_css_selector("div[role='dialog']"))
        dialog_box = self.browser.find_element_by_class_name("ui-dialog")
        self.assertIn('Grid was created.', dialog_box.text)
        

class UpdateGridTest(BaseLiveTest):
    fixtures = ['grid_admin_user.json']
    
    def test_can_update_grid(self):
        BaseLiveTest.can_login(self)
        
        # User clicks 'Grids' link and sees the my grids page
        grids_link = self.browser.find_element_by_link_text("Grids")
        grids_link.click()
        
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Grid Management', body.text)
            
        # The 'select' tag contains the created grid with name 'grid1'
        select_field = self.browser.find_element_by_css_selector("select")
        self.assertIn('grid1', select_field.text)
        
        # User selects the option with grid name 'grid1' and sees the grid with the
        # name 'grid1' in the input text.
        option_fields = self.browser.find_elements_by_css_selector('option')
        option_fields[1].click()
        
        WebDriverWait(self.browser, 10).until(lambda x: self.browser.find_element_by_id("gridTrableContainerDiv"))
        grid_name_field = self.browser.find_element_by_name("gridName")
        self.assertEquals('grid1', grid_name_field.get_attribute('value'))
        
        # User changes the name of the grid to 'grid123', adds a column and a row
        grid_name_field.send_keys('23')
        
        self.browser.find_element_by_class_name("colMenu").mouseOver()
        self.browser.find_element_by_class_name("addImage").click()
        
        
        
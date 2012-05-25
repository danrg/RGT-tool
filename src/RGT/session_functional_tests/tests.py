"""
This file is used for the functional tests related to session operations,
using the selenium module. These will pass when you run "manage.py test session_functional_tests".

"""
from RGT.base_functional_tests.tests import BaseLiveTest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
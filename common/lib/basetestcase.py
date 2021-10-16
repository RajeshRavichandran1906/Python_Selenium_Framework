import unittest
from common.lib.utillity import UtillityMethods
from common.lib.global_variables import Global_variables
from common.lib.webdriverfactory.webdriverfactory import WebDriverFactory

class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        browser = UtillityMethods.parseinitfile(self,'browser')
        UtillityMethods.kill_browser_process(self)
        self.driver = WebDriverFactory().getInstance(browser)
        Global_variables.webdriver = self.driver
        self.driver.maximize_window()
        UtillityMethods.windows=self.driver.window_handles
        Global_variables.windows_handles=self.driver.window_handles
        Global_variables.current_test_case=self._testMethodName.replace('test_', '').strip()
        BRWSR_NAME=self.driver.desired_capabilities['browserName'].lower()
        Global_variables.browser_name=BRWSR_NAME
    
    def tearDown(self):
        self.driver.quit()

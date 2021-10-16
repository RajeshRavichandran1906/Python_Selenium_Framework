from common.lib.basetestcase import BaseTestCase
from common.lib.utillity import UtillityMethods
from common.lib.global_variables import Global_variables

class TC1_TestClass(BaseTestCase):
    
    def test_TC_1(self):
        
        """
            TEST CASE OBJECTS
        """
        driver = Global_variables.webdriver
        utils = UtillityMethods(driver)
        
    
        driver.get("http://www.google.com")
        window_title = driver.title
        msg = "Step 01: Verify browser Title"
        utils.asequal('Google', window_title, msg)
        

        

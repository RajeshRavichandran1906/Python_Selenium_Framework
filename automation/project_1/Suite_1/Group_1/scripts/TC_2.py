from common.lib.basepage import BasePage
from common.lib.basetestcase import BaseTestCase

class TC2_TestClass(BaseTestCase):
    
    def test_TC_2(self):
        
        """
            TEST CASE OBJECTS
        """
        Base = BasePage()
        
        """
            TEST CASE VARIABLES
        """
        login_button = (Base._By.CSS_SELECTOR, "#LoginButton")
        user_name = (Base._By.CSS_SELECTOR, "input#User")
        password = (Base._By.CSS_SELECTOR, "input#Password")
        project_1 = (Base._By.CSS_SELECTOR, "input#ProjectID1_Search")
        project_2 = (Base._By.CSS_SELECTOR, "input#ProjectID2_Search")
        project_3 = (Base._By.CSS_SELECTOR, "input#ProjectID3_Search")
        Task_1 = (Base._By.CSS_SELECTOR, "input#ActionID1_Search")
        Task_2 = (Base._By.CSS_SELECTOR, "input#ActionID2_Search")
        Task_3 = (Base._By.CSS_SELECTOR, "input#ActionID3_Search")
        remark_1 = (Base._By.CSS_SELECTOR, "input#Remark1")
        remark_2 = (Base._By.CSS_SELECTOR, "input#Remark2")
        remark_3 = (Base._By.CSS_SELECTOR, "input#Remark3")
        start_1 = (Base._By.CSS_SELECTOR, "input#StartTime1")
        start_2 = (Base._By.CSS_SELECTOR, "input#StartTime2")
        start_3 = (Base._By.CSS_SELECTOR, "input#StartTime3")
        end_1 = (Base._By.CSS_SELECTOR, "input#EndTime1")
        end_2 = (Base._By.CSS_SELECTOR, "input#EndTime2")
        end_3 = (Base._By.CSS_SELECTOR, "input#EndTime3")
        project_list_item_parent = (Base._By.CSS_SELECTOR, "div[id*='Project'][id$='Select']")
        project_list_items = (Base._By.CSS_SELECTOR, project_list_item_parent[1] + " li")
        task_list_item_parent = (Base._By.CSS_SELECTOR, "div[id^='Action'][id$='Select']")
        task_list_items = (Base._By.CSS_SELECTOR, task_list_item_parent[1] + " li")
        submit_button = (Base._By.CSS_SELECTOR, "button.Primary.CallForAction")
        message_box = (Base._By.CSS_SELECTOR, "div[class='MessageBox Notice'] p")
    
        def select_list_item(list_item, list_locator):
            list_options = Base._utils.validate_and_get_webdriver_objects_using_locator(list_locator, "List Options")
            list_option = Base._javascript.find_elements_by_text(list_options, list_item)      
            Base._javascript.scrollIntoView(list_option[0])
            Base._utils.left_click(list_option[0], action_chain_click=True)
        
        "Step 1"
        Base._driver.get("https://otrs.amtexsystems.com/otrs/")
        Base._webelement.wait_for_element_text(login_button, "Login", 30)
        
        "Step 2"
        user_name_obj = Base._utils.validate_and_get_webdriver_object_using_locator(user_name, "User Name")
        user_name_obj.send_keys("rajesh")
        
        password_obj = Base._utils.validate_and_get_webdriver_object_using_locator(password, "Password")
        password_obj.send_keys("Amtex123")
        
        login_button_obj = Base._utils.validate_and_get_webdriver_object_using_locator(login_button, "Login Button")
        login_button_obj.click()
        Base._webelement.wait_for_element_text(submit_button, "Submit", 30)
        
        "Step 3"
        Base._utils.validate_and_get_webdriver_object_using_locator(project_1, "Project 1").click()
        Base._webelement.wait_until_element_visible(project_list_item_parent, 30)
        select_list_item("IBIQA Team", project_list_items)
        Base._webelement.wait_until_element_invisible(project_list_item_parent, 30)
        
        Base._utils.validate_and_get_webdriver_object_using_locator(project_2, "Project 2").click()
        Base._webelement.wait_until_element_visible(project_list_item_parent, 30)
        select_list_item("IBIQA Team", project_list_items)
        Base._webelement.wait_until_element_invisible(project_list_item_parent, 30)
        
        Base._utils.validate_and_get_webdriver_object_using_locator(project_3, "Project 3").click()
        Base._webelement.wait_until_element_visible(project_list_item_parent, 30)
        select_list_item("IBIQA Team", project_list_items)
        Base._webelement.wait_until_element_invisible(project_list_item_parent, 30)
          
        Base._utils.validate_and_get_webdriver_object_using_locator(Task_1, "Task 1").click()
        Base._webelement.wait_until_element_visible(task_list_item_parent, 30)
        select_list_item("IBIQA - Automation - New Development", task_list_items)
        Base._webelement.wait_until_element_invisible(task_list_item_parent, 30)
        
        Base._utils.validate_and_get_webdriver_object_using_locator(Task_2, "Task 2").click()
        Base._webelement.wait_until_element_visible(task_list_item_parent, 30)
        select_list_item("IBIQA - Automation - Function creation", task_list_items)
        Base._webelement.wait_until_element_invisible(task_list_item_parent, 30)
        
        Base._utils.validate_and_get_webdriver_object_using_locator(Task_3, "Task 3").click()
        Base._webelement.wait_until_element_visible(task_list_item_parent, 30)
        select_list_item("IBIQA - Other Activities", task_list_items)
        Base._webelement.wait_until_element_invisible(task_list_item_parent, 30)
        
        Base._utils.validate_and_get_webdriver_object_using_locator(remark_1, "Remarks 1").send_keys("Involved in DF Development")
        Base._utils.validate_and_get_webdriver_object_using_locator(remark_2, "Remarks 1").send_keys("Involved in DF Function Creation")
        Base._utils.validate_and_get_webdriver_object_using_locator(remark_3, "Remarks 1").send_keys("Involved in Suite Run Maintainance")
        
        Base._utils.validate_and_get_webdriver_object_using_locator(start_1, "Start 1").send_keys("11:00")
        Base._utils.validate_and_get_webdriver_object_using_locator(start_2, "Start 2").send_keys("15:00")
        Base._utils.validate_and_get_webdriver_object_using_locator(start_3, "Start 3").send_keys("20:00")
        
        Base._utils.validate_and_get_webdriver_object_using_locator(end_1, "End 1").send_keys("14:00")
        Base._utils.validate_and_get_webdriver_object_using_locator(end_2, "End 2").send_keys("20:00")
        Base._utils.validate_and_get_webdriver_object_using_locator(end_3, "End 2").send_keys("20:45")
        
        Base._utils.left_click(Base._utils.validate_and_get_webdriver_object_using_locator(submit_button, "Submit Button"), action_chain_click=True)
        Base._webelement.wait_for_element_text(message_box, "Successful", 30)
        actual = Base._utils.validate_and_get_webdriver_object_using_locator(message_box, "Message Box").text
        msg = "Step 01: Successfully insert the data in OTRS"
        Base._utils.asequal("Successful insert!", actual, msg)        
        
        
import time
from common.lib.javascript import JavaScript
from common.lib.utillity import UtillityMethods
from selenium.webdriver.support.color import Color
from common.lib.global_variables import Global_variables
from selenium.webdriver.remote.webelement import WebElement

class WebElementUtils:
    
    def __init__(self):
        
        self._driver = Global_variables.webdriver
        self._utils = UtillityMethods(self._driver) 
        self._javascript = JavaScript(self._driver)
        
    def verify_elements_text(self, elements_instance, expected_text, step_num, element_name, assert_type="equal", value_len=None, slicing=(None, None), parent_instance=None):
        """
        Description: Verify the web elements text
        """
        actual_text_list = self.get_elements_text(elements_instance, parent_instance)
        self._utils.list_values_verification(expected_text, actual_text_list, step_num, element_name, assert_type, value_len, slicing)
    
    def verify_number_of_visible_elements(self, elements_instance, expected_count, msg, parent_instance=None):
        """
        Description: Verify the visible number of elements
        """
        elements = self._get_objects(elements_instance, parent_instance)
        actual_count = sum([1 for element in elements if element.is_displayed()])
        self._utils.asequal(expected_count, actual_count, msg)
        
    def get_elements_text(self, elements_instance, parent_instance=None):
        
        elements_instance = self._get_objects(elements_instance, parent_instance)
        return [element.text.strip() for element in elements_instance if element.is_displayed()]
    
    def verify_element_color_by_css_property(self, elements_instance, property_name, color_name, msg, element_name):
        
        actual_color = Color.from_string(self._get_object(elements_instance, element_name).get_attribute(property_name)).rgba
        expected_color = self._utils.color_picker(color_name, 'rgba')
        self._utils.asequal(expected_color, actual_color, msg)
    
    def wait_for_element_text(self, locator, element_text, time_out, pause_time=0, case_sensitive=False, raise_error=True, javascript=False, parent_obj=None):
        """
        Description: WebDriver will wait until given text visible on given locator
        """
        end_time=time.time()+time_out
        while True :
            if time.time()>end_time :
                if raise_error:
                    msg = "Time out for find [{}] text in [{}] element".format(element_text, locator)
                    raise TimeoutError(msg)
                else:
                    return False
            try :
                element = parent_obj.find_element(*locator) if parent_obj else self._driver.find_element(*locator)
                actual_text = self._javascript.get_element_text(element) if javascript else element.text
                if case_sensitive != True:
                    actual_text = actual_text.lower().replace(" ", "").replace("\n", "")
                    element_text = element_text.lower().replace(" ", "")
                if element_text in actual_text :
                    time.sleep(pause_time)
                    return element
            except :
                pass
            time.sleep(0.5)
    
    def wait_until_element_visible(self, locator, time_out, pause_time=0, raise_error=True, parent_obj=None):
        """
        Description: WebDriver will wait until element visible
        """
        end_time=time.time()+time_out
        while True :
            if time.time()>end_time :
                if raise_error:
                    msg = "Time out for get visibility status of element".format(locator)
                    raise TimeoutError(msg)
                else:
                    return False
            try :
                element = parent_obj.find_element(*locator) if parent_obj else self._driver.find_element(*locator)
                if element.is_displayed():
                    time.sleep(pause_time)
                    return element
            except :
                pass
            time.sleep(0.5)
    
    def wait_until_element_invisible(self, locator, time_out, pause_time=0, raise_error=True, parent_obj=None):
        """
        Description: WebDriver will wait until element invisible
        """
        end_time=time.time()+time_out
        while True :
            if time.time()>end_time :
                if raise_error:
                    msg = "Time out for get visibility status of element".format(locator)
                    raise TimeoutError(msg)
                else:
                    return False
            try :
                elements = parent_obj.find_elements(*locator) if parent_obj else self._driver.find_elements(*locator)
                if elements == [] or not elements[0].is_displayed():
                    time.sleep(pause_time)
                    return True
            except :
                pass
            time.sleep(0.5)
            
    def _get_objects(self, element_instance, parent_instance=None):
        
        is_locator = isinstance(element_instance, tuple) and len(element_instance) == 2
        if is_locator:
            if parent_instance:
                return parent_instance.find_elements(*element_instance)
            return self._driver.find_elements(*element_instance)
        if isinstance(element_instance, list):
            return element_instance
        else:
            raise TypeError("Element instance should be WebElements list or Locator")
    
    def _get_object(self, element_instance, element_name):
    
        is_locator = isinstance(element_instance, tuple) and len(element_instance) == 2
        if is_locator:
            return self._utils.validate_and_get_webdriver_object_using_locator(element_instance, element_name)
        elif isinstance(element_instance, WebElement):
            return element_instance
        else:
            raise TypeError("Element instance should be WebElement or Locator")
        


            
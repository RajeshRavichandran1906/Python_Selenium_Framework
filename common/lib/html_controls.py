import time
import keyboard
from common.lib.javascript import JavaScript
from common.lib.utillity import UtillityMethods
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.select import Select
from common.lib.global_variables import Global_variables


class _base_:
    
    def __init__(self):
        
        self._utils_      =  UtillityMethods(Global_variables.webdriver)
        self._javascript_ = JavaScript(Global_variables.webdriver)
        
        
class TextBox(_base_):
    
    def __init__(self, textbox_object, textbox_name):
        
        self._object  = textbox_object
        self._name_   = textbox_name
        self._delay_  = 0 # Typing speed delay time
        super(TextBox, self).__init__()
        
    def enter_text(self, value, clear=True):
        """
        Description : Enter the text in textbox.
        :param - clear = Clear the text before enter if True 
        """
        clear and self.clear()
        self.click()
        keyboard.write(value, delay=self._delay_)
    
    def clear(self):
        """
        Description : Left click on textbox
        """
        self.click()
        time.sleep(0.5)
        keyboard.send("ctrl+a")
        time.sleep(0.5)
        keyboard.send("del")
        time.sleep(0.5)
    
    def click(self):
        """
        Description : Left click on textbox
        """
        self._core_utils_.python_left_click(self._object)
    
    def verify_text(self, expected_text, step_num):
        """
        Description : Verify the textbox vlaue
        :Usage - verify_text("Folder 1", "01.02")
        """
        actual_text = self._object.get_attribute('value').strip()
        msg = "Step {0} : Verify [{1}] displayed in [{2}] textbox".format(step_num, expected_text, self._name_)
        self._utils_.asequal(expected_text, actual_text, msg)
        
    def verify_contains_text(self, expected_text, step_num):
        """
        Description : Verify the value present in textbox.
        :Usage - verify_contains_text("Folder 1", "01.02")
        """
        actual_text = self._object.get_attribute('value').strip()
        msg = "Step {0} : Verify [{1}] present in [{2}] textbox".format(step_num, expected_text, self._name_)
        self._utils_.asin(expected_text, actual_text, msg)
        
    def verify_placeholder(self, expected_placeholder, step_num):
        """
        Description : Verify the textbox placeholder value
        :Usage - verify_placeholder("Enter the user", "01.02")
        """
        actual_value = self._object.get_attribute('value').strip()
        actual_value = self._object.get_attribute('placeholder').strip() if actual_value == '' else actual_value
        msg = "Step {0} : Verify [{1}] placeholder displayed in [{2}] textbox".format(step_num, expected_placeholder, self._name_)
        self._utils_.asequal(expected_placeholder, actual_value, msg)
        
    def verify_read_only(self, step_num):
        """
        Description : Verify whether textbox is readonly 
        :Usage - verify_read_only("01.02")
        """
        readonly = self._object.get_attribute('readonly')
        msg = "Step {0} : Verify [{1}] textbox is read only".format(step_num, self._name_)
        self._utils_.asequal('true', readonly, msg)
        
    def verify_editable(self, step_num):
        """
        Description : Verify whether textbox is Editable 
        :Usage - verify_editable("01.02")
        """
        readonly = self._object.get_attribute('readonly')
        msg = "Step {0} : Verify [{1}] textbox is editable".format(step_num, self._name_)
        self._utils_.asequal(None, readonly, msg)
    
    def verify_border_color(self, expected_color, step_num):
        """
        Description : Verify the textbox border color
        """
        expected_color = [self._utils_.color_picker(expected_color)] * 4
        border_directions = ['border-left-color', 'border-top-color', 'border-right-color', 'border-bottom-color']
        actual_color = [Color.from_string(self._object.value_of_css_property(boder)).rgb for boder in border_directions]
        msg = "Step {0} : Verify [{1}] textbox highlighted with [{2}] border color".format(step_num, self._name_, expected_color[0])
        self._utils_.asequal(expected_color, actual_color, msg)


class Button(_base_):
    
    def __init__(self, button_object, button_name):
        
        self._object_ = button_object
        self._name_   = button_name
        super(Button, self).__init__()
    
    def click(self):
        """
        Description : Left click on Button
        """
        self._core_utils_.left_click(self._object_)
    
    def verify_text(self, expected_text, step_num):
        """
        Description : Verify the button text
        """
        actual_text = self._object_.text.strip()
        msg = 'Step {0} : Verify [{1}] button displayed with [{2}] text'.format(step_num, self._name_, expected_text)
        self._utils_.asequal(expected_text, actual_text, msg)
        
        
class DropDown(_base_):
    
        def __init__(self, select_object, object_name):
        
            super().__init__()
            self._select_ = Select(select_object)
            self._object_name_ = object_name
        
        def select(self, option_name):
            """
            Description : Select the given option from select control.
            """
            self._select_.select_by_visible_text(option_name)
            
        def verify_selected_option(self, expected, step_num):
            """
            Description Verify the selected option in dropdown controls
            """
            actual = self._select_.first_selected_option.text.strip()
            msg = "Step {0} : Verify [{1}] option selected in [{2}]".format(step_num, expected, self._object_name_)
            self._utils_.asequal(expected, actual, msg)
            
            
class RadioButton(_base_):
    pass


class CheckBox(_base_):
    
    def __init__(self, object_, object_name):
        
        super().__init__()
        self._object_ = object_
        self._object_name = object_name
    
    def check(self):
        """
        Description : Click on check box if check box not checked
        """
        ("uncheck" in self._object_.get_attribute('class')) and self._core_utils_.left_click(self._object_)
    
    def uncheck(self):
        """
        Description : Click on check box if check box is checked
        """
        ("uncheck" not in self._object_.get_attribute('class')) and self._core_utils_.left_click(self._object_)
        
    def verify_checked(self, step_num):
        """
        Description: Verify whether check box is checked
        """
        msg = "Step {0} : Verify [{1}] CheckBox is checked".format(step_num, self._object_name)
        marker_value = self._javascript_.get_element_before_style_properties(self._object_, "content")
        state = True if marker_value == '"\ue834"' else False
        self._utils_.asequal(True, state, msg)
    
    def verify_unchecked(self, step_num):
        """
        Description : Verify whether check box is unchecked
        """
        msg = "Step {0} : Verify [{1}] CheckBox is unchecked".format(step_num, self._object_name)
        marker_value = self._javascript_.get_element_before_style_properties(self._object_, "content")
        state = True if marker_value == '"\ue835"' else False
        self._utils_.asequal(True, state, msg)
       
        
class File(_base_):
    pass    


class Label(_base_):
    
    def __init__(self, Label_object, Label_name):
        
        self._object_ = Label_object
        self._name_   = Label_name
        super(Label, self).__init__()
    
    def verify_text(self, expected_text, step_num):
        """
        Description : Verify the label text
        :Usage - verify_text('Testing', '04.01')
        """
        actual_text = self._object_.text.strip()
        msg = 'Step {0} : Verify [{1}] displayed in [{2}] label'.format(step_num, expected_text, self._name_)
        self._utils_.asequal(expected_text, actual_text, msg)
    
    def verify_not_displayed(self, step_num):
        """
        Description : Verify whether label element not displayed
        :Usage - verify_not_displayed('Testing', '04.01')
        """
        msg = 'Step {0} : Verify [{1}] label not displayed'.format(step_num, self._name_)
        self._utils_.asequal(False, self._object_.is_displayed(), msg)
        
    def verify_background_color(self, expected_color, step_num):
        """
        Description : Verify the label background color
        :Usage - verify_text('Testing', '04.01')
        """
        msg = 'Step {0} : Verify [{1}] label displayed with [{2}] background color'.format(step_num, self._name_, expected_color)
        self._utils_.verify_element_color_using_css_property(None, expected_color, msg, attribute='background-color', element_obj=self._object_)
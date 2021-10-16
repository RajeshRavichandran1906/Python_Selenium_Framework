import time


class JavaScript :
    
    def __init__(self, driver):
        self.driver=driver
    
    def get_elements_text(self, elements_object):
        """
        This method used to find given css elements and return elements text as list
        Note : Do Not use for Verification (Will return invisible text also)
        """
        script="text=[];for(i=0;i<arguments[0].length;i++){text.push(arguments[0][i].innerText.trim())}return text"
        elements_text=self.driver.execute_script(script, elements_object)
        return elements_text
    
    def get_element_text(self, element_obj):
        """
        This method is used to get the text of single element
        """
        script = "return arguments[0].innerText"
        element_text = self.driver.execute_script(script, element_obj)
        return element_text
        
    def find_elements_by_text(self, elements_object, text_to_find):
        """
        This method used to find elements by given text. It will return element as list if given text found
        """ 
        script="elements=[]; for (i=0;i<arguments[0].length;i++){if(arguments[0][i].innerText.trim()=='" + text_to_find + "'){elements.push(arguments[0][i])}} return elements"
        foud_elements=self.driver.execute_script(script, elements_object)
        return (foud_elements)
    
    def scroll_element(self, scrollable_element_css, scroll_offset, wait_time=0):
        """
        This method used to scroll the element based on scroll_offset value. element should be have scrollable 
        """
        script ='document.querySelector("' + scrollable_element_css + '").scrollTop=' + str(scroll_offset) 
        self.driver.execute_script(script)
        time.sleep(wait_time)
        
    def get_element_property_value(self, element_object,property_name):
        """
        This method used to get element property like scrollTop, textContent and etc
        """
        script ="return arguments[0]." + property_name
        property_value=self.driver.execute_script(script, element_object) 
        return property_value
    
    def check_scroll_is_completed(self, scrollable_element_css):
        """
        This method used to check whether scroll is completed which means scroll bar reached bottom of the element
        """
        scrollable_element_object=self.driver.find_element_by_css_selector(scrollable_element_css)
        script="return arguments[0].offsetHeight + arguments[0].scrollTop == arguments[0].scrollHeight"
        status=self.driver.execute_script(script, scrollable_element_object)
        return status
    
    def get_scroll_offsetTop(self, element_object):
        """
        This method used to get element scroll offsetTop value
        """
        return JavaScript.get_element_property_value(self, element_object, 'offsetTop')
    
    def scrollTop(self, scrollable_element_css, scroll_to_element_obj, wait_time=2):
        """
        This function used to scroll the given scrollable element based of scroll_to_element offsetTop value
        """
        scrolltop_value=self.driver.execute_script('return arguments[0].offsetTop', scroll_to_element_obj)
        scroll_script_syntax='document.querySelector("{0}").scrollTop={1}'.format(scrollable_element_css, scrolltop_value)
        self.driver.execute_script(scroll_script_syntax)
        time.sleep(wait_time)
    
    def get_scroll_offsetLeft(self, element_object):
        """
        This method used to get element scroll offsetTop value
        """
        return JavaScript.get_element_property_value(self, element_object, 'offsetLeft')
    
    def scrollLeft(self, scrollable_element_object, scroll_to_element_obj, wait_time=1):
        """
        This function used to scroll the given scrollable element based of scroll_to_element offsetTop value
        """
        offsetLeft=JavaScript.get_scroll_offsetLeft(self, scroll_to_element_obj)
        scroll_script_syntax='arguments[0].scrollLeft={0}'.format(offsetLeft)
        self.driver.execute_script(scroll_script_syntax, scrollable_element_object)
        time.sleep(wait_time)
    
    def find_element_index_by_text(self, elements_object, text_to_find, index_to_start=0):
        """
        This method used to find element index by given text. It will return element index if given text match otherwise None will return
        :arg - index_to_start = From which row start to find element text 
        """ 
        script="for(i=arguments[1];i<arguments[0].length;i++){if(arguments[0][i].innerText.trim()=='" + text_to_find + "'){return i; break;}}"
        foud_elements=self.driver.execute_script(script, elements_object, index_to_start)
        return (foud_elements)
    
    def find_all_index_of_element_by_text(self, elements_object, text_to_find, index_to_start=0):
        """
        This method used to find element index by given text. It will return element index if given text match otherwise empty will return
        :arg - index_to_start = From which row start to find element text 
        """ 
        script="found_index=[]; for(i=arguments[1];i<arguments[0].length;i++){if(arguments[0][i].innerText.trim()=='" + text_to_find + "'){found_index.push(i);}} return found_index;"
        foud_index_list=self.driver.execute_script(script, elements_object, index_to_start)
        return (foud_index_list)
    
    def scrollIntoView(self, element_obj, wait_time=2):
        """
        If the element is fully within the visible area of the viewport, it does nothing. Otherwise, 
        the element is scrolled into view
        """
        scroll_script_syntax='arguments[0].scrollIntoView()'
        self.driver.execute_script(scroll_script_syntax, element_obj)
        time.sleep(wait_time)
    
    def scroll_into_view_ifneeded(self, element_obj, wait_time=2):
        """
        Description: This function scrolls and makes the object visible if it not visible
        :usage : scroll_into_view_ifneeded(element_obj)
        """
        scroll_script_syntax='arguments[0].scrollIntoViewIfNeeded()'
        self.driver.execute_script(scroll_script_syntax, element_obj)
        time.sleep(wait_time)
    
    def get_element_before_style_properties(self, element_obj, property_name):
        """
        This method used to get element ::before style properties
        use of ::before = ::before pseudo-elements are used for styling of containing element.
        """
        script="return window.getComputedStyle(arguments[0], ':before').getPropertyValue('{0}')".format(property_name)
        property_value=self.driver.execute_script(script, element_obj)
        return property_value
    
    def get_element_after_style_properties(self, element_obj, property_name):
        """
        This method used to get element ::before style properties
        use of ::before = ::before pseudo-elements are used for styling of containing element.
        """
        script="return window.getComputedStyle(arguments[0], ':after').getPropertyValue('{0}')".format(property_name)
        property_value=self.driver.execute_script(script, element_obj)
        return property_value
    
    def get_element_all_attributes(self, element_obj):
        '''
        This function will return all attributes and it's value of object.
        @Aftab Alam Khan 
        '''
        element_attributes_dict=self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element_obj)
        return (element_attributes_dict)
    
    def check_vertical_scroll_reached_bottom(self, scrollable_element_obj):
        """
        This method used to check whether vertical scroll bar reached bottom of the given element object. It will True if vertical scroll reached bottom of the element else False
        """
        script="return arguments[0].offsetHeight + arguments[0].scrollTop == arguments[0].scrollHeight + (arguments[0].offsetHeight - arguments[0].clientHeight)"
        status=self.driver.execute_script(script, scrollable_element_obj)
        return status
    
    def check_element_has_vertical_scrollbar(self, scrollable_element_obj):
        """
        This method used to check whether given element has vertical scroll bar. It will True if if element has vertical scroll else False
        """
        script="return arguments[0].scrollHeight > arguments[0].clientHeight"
        status=self.driver.execute_script(script, scrollable_element_obj)
        return status
    
    def check_element_has_horizontal_scrollbar(self, scrollable_element_obj):
        """
        This method used to check whether given element has horizontal scroll bar. It will True if if element has horizontal scroll else False
        """
        script="return arguments[0].scrollWidth > arguments[0].clientWidth"
        status=self.driver.execute_script(script, scrollable_element_obj)
        return status
    
    def is_image_loaded_in_img_tag(self, img_tab_object):
        """
        Description : This method will return True if image loaded properly in img tag else False
        :arg - img_tab_object : selenium object of img tag  
        """
        script = "return arguments[0].naturalWidth != 0 && arguments[0].complete"
        status=self.driver.execute_script(script, img_tab_object)
        return status
    
    def wait_for_page_loads(self, time_out, sleep_interval=0.5, pause_time=1) :
        """
        Webdriver will wait until complete the page load
        """
        script = "return document.readyState"
        end_time=time.time()+time_out
        while True :
            time.sleep(sleep_interval)
            if time.time()>end_time :
                msg = "'{0}' page took more than {0} seconds to load".format(self.driver.title, time_out)
                print(msg)
                break
            try :
                page_status = self.driver.execute_script(script)
                if page_status.strip() == "complete" :
                    time.sleep(pause_time)
                    break
            except :
                pass
    
    def get_parent_element(self, element_obj):
        """
        Return the parent element object of given element 
        """
        script="return arguments[0].parentElement"
        parent_element=self.driver.execute_script(script, element_obj)
        return parent_element
    
    def get_child_elements(self, element_obj):
        """
        Return the all child elements object of given element 
        """
        script="return arguments[0].childNodes"
        parent_element=self.driver.execute_script(script, element_obj)
        return parent_element
    
    def get_highlighted_text(self):
        """
        Returns all the highlighted text in the page
        """
        script = "return window.getSelection().toString();"
        highlighted_text = self.driver.execute_script(script)
        return highlighted_text.strip()
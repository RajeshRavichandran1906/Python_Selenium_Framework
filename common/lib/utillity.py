from uisoup import uisoup
from PIL import Image, ImageGrab
from common.lib import root_path
from common.lib.javascript import JavaScript
from selenium.webdriver.support.color import Color
from configparser import ConfigParser, NoOptionError
import re, os, sys, time, unittest, pyautogui, psutil
from common.lib.global_variables import Global_variables
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

class UtillityMethods:
    
    def __init__(self, driver):
        self.driver = driver
    
    def validate_and_get_webdriver_object_using_locator(self, locator, webdriver_object_name, parent_object=None):
        '''
        This function is used to validate the webdriver object
        css_locator: css will be provided by User(#TableChart_1)
        webdriver_object_name: The meaningful and related name of the object will be provided by User.(Preview chart)
        '''
        try:
            if parent_object != None:
                return parent_object.find_element(*locator)
            else:
                return self.driver.find_element(*locator)
        except NoSuchElementException:
            display_msg = "{0} is currently not available in the page. The Provided CSS attribute ['{1}'] might not be correct.".format(webdriver_object_name, locator)
            raise AttributeError(display_msg)
    
    def validate_and_get_webdriver_objects_using_locator(self, locator, webdriver_objects_reference_name, parent_object=None):
        '''
        This function is used to verify the list of webdriver elements in the page
        css_locator: css will be provided by User((#TableChart_1)
        webdriver_objects_reference_name : The meaningful and related name of the objects will be provided by User.(Preview chart)
        '''
        if parent_object != None:
            resp = parent_object.find_elements(*locator)
        else:
            resp = self.driver.find_elements(*locator)
        if len(resp) == 0:
            display_msg = "{0} is currently not available in the page. The Provided CSS attribute ['{1}'] might not be correct.".format(webdriver_objects_reference_name, locator)
            raise AttributeError(display_msg)
        else:
            return resp
          
    def toLog(self, *args):
        fileObj = open("D:\\log.txt", "a")
        for arg in args:
            fileObj.write(arg)
            fileObj.write("\n")
        fileObj.close()
    
    def parseinitfile(self, key):
        init_file = 'config.init'
        config_pair = {}
        try:
            fileObj = open(init_file, "r")
            line = fileObj.readline()
            while line:
                lineObjbj = re.match(r'(\S*)\s(.*)', line)
                keyName = lineObjbj.group(1)
                config_pair[keyName] = lineObjbj.group(2)
                line = fileObj.readline()
            fileObj.close()
        except IOError:
            exit()
        if key in config_pair:
            return (config_pair[key])
        else:
            return ('Key not found')
        
    def verify_current_tab_name(self, tab_name, msg):
        '''
        This will verify current window tab name
        @param alias_url_path: This url is after alias location
        :Usage verify_tab_name('portal', 'Step 9')
        '''
        current_tab_name = self.driver.title
        UtillityMethods.asequal(self, tab_name, current_tab_name, msg)
        
    def kill_browser_process(self):
        '''
        This function will kill browser, browser driver and python shell process.
        
        :Usage kill_browser_process()
        '''
        for proc in psutil.process_iter():
            try:
                # Get process name from process object.
                processName = proc.name()
                if processName in ['chromedriver.exe', 'geckodriver.exe', 'IEDriverServer.exe', 'MicrosoftWebDriver.exe', 'chrome.exe', 'firefox.exe', 'MicrosoftEdge.exe', 'iexplore.exe']:
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            
    def get_user_name(self):
        '''
        Description: This method will get all username and password from config file and store in global variable used_username_in_current_session as dict form.
        '''
        try:
            init_file = 'config.init'
            fileObj = open(init_file, "r")
            line = fileObj.readline().replace('\n','')
            while line:
                if 'mr' in line:
                    username = line.split(' ')
                    line = fileObj.readline().replace('\n','')
                    password_ = line.split(' ')
                    try:
                        Global_variables.used_username_in_current_session[username[1]] = password_[1]
                    except IndexError:
                        Global_variables.used_username_in_current_session[username[1]] = ''
                line = fileObj.readline().replace('\n','')
            fileObj.close()
        except Exception as e:
            print(Exception(e))

    def synchronize_with_number_of_element(self, element_css, expected_number, expire_time, pause_time=1):
        '''
        This function synchronize with expected number of element in current browser.
        :param parent_css:-element css need to pass
        :param expected_number:-0, 1, 2,........
        :param expire_time:-1, 5,........
        :param pause_time=0.2,1...
        :Usage synchronize_with_number_of_element("[id*='RangeValuesBox'] [id*='From'] > input", 1, 190)
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_obj = self.driver.find_elements_by_css_selector(element_css)
                check_obj_exist = temp_obj[0]
                del check_obj_exist
            except IndexError:
                time.sleep(pause_time)
                continue
            except TypeError:
                time.sleep(pause_time)
                continue
            if len(temp_obj) == int(expected_number):
                run_=False
                break
            else:
                time.sleep(pause_time)
        time.sleep(pause_time)
        
    def synchronize_with_number_of_element_within_parent_object(self, parent_object, element_css, expected_number, expire_time, pause_time=1):
        '''
        This function synchronize with expected number of element in current browser.
        :param parent_css:-element css need to pass
        :param expected_number:-0, 1, 2,........
        :param expire_time:-1, 5,........
        :param pause_time=0.2,1...
        :Usage synchronize_with_number_of_element("[id*='RangeValuesBox'] [id*='From'] > input", 1, 190)
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_obj = parent_object.find_elements_by_css_selector(element_css)
                check_obj_exist = temp_obj[0]
                del check_obj_exist
            except IndexError:
                time.sleep(pause_time)
                continue
            except TypeError:
                time.sleep(pause_time)
                continue
            if len(temp_obj) == int(expected_number):
                run_=False
                break
            else:
                time.sleep(pause_time)
        time.sleep(pause_time)
    
    def synchronize_with_visble_text(self, element_css, visble_element_text, expire_time, pause_time=1, text_option='dom_visible_text', condition_type='asin'):
        '''
        This function synchronize with expected visible text of element in current browser.
        :param parent_css:-element css need to pass
        :param visble_element_text:-visible text need to pass
        :param expire_time:-1, 5,........
        :param pause_time=0.2,1...
        :usage utillityobject.synchronize_with_visble_text(self, "[id*='RangeValuesBox'] [id*='From'] > input", '2014', 190, text_option='text_value')
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_str_value_elem=self.driver.find_element_by_css_selector(element_css)
                temp_str_value=UtillityMethods.get_attribute_value(self, temp_str_value_elem, text_option)
            except NoSuchElementException:
                time.sleep(pause_time)
                continue
            except StaleElementReferenceException:
                time.sleep(pause_time)
                continue
            str_value = re.sub(' ','',temp_str_value[text_option]).replace('\n','')
            if condition_type == 'asin':
                if str(visble_element_text.replace(' ','')) in str_value:
                    run_=False
                    break
                else:
                    time.sleep(pause_time)
            elif condition_type == 'asnotin':
                if str(visble_element_text.replace(' ','')) not in str_value:
                    run_=False
                    break
                else:
                    time.sleep(pause_time)
        time.sleep(pause_time)
    
    def synchronize_with_visble_text_within_parent_object(self, parent_object, element_css, visble_element_text, expire_time, pause_time=1, text_option='dom_visible_text'):
        '''
        This function synchronize with expected visible text of element in current browser.
        :param parent_css:-element css need to pass
        :param visble_element_text:-visible text need to pass
        :param expire_time:-1, 5,........
        :param pause_time=0.2,1...
        :usage utillityobject.synchronize_with_visble_text(self, "[id*='RangeValuesBox'] [id*='From'] > input", '2014', 190, text_option='text_value')
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_str_value_elem=parent_object.find_element_by_css_selector(element_css)
                temp_str_value=UtillityMethods.get_attribute_value(self, temp_str_value_elem, text_option)
            except NoSuchElementException:
                time.sleep(pause_time)
                continue
            except StaleElementReferenceException:
                time.sleep(pause_time)
                continue
            str_value = re.sub(' ','',temp_str_value[text_option]).replace('\n','')
            if str(visble_element_text.replace(' ','')) in str_value:
                run_=False
                break
            else:
                time.sleep(pause_time)
        time.sleep(pause_time)
    
    def synchronize_until_element_disappear(self, element_css, expire_time, pause_time=1):
        '''
        This function is used to check the length of element reduced.
        :Usage synchronize_until_element_disappear("[id*='RangeValuesBox']", 9)
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_obj = self.driver.find_element_by_css_selector(element_css).is_displayed()
            except NoSuchElementException:
                time.sleep(pause_time)
                temp_obj = False
            if temp_obj == False:
                run_=False
                break
            else:
                time.sleep(pause_time)
                continue
        time.sleep(pause_time)
    
    def synchronize_until_element_disappear_within_parent_object(self, parent_object, element_css, expire_time, pause_time=1):
        '''
        This function is used to check the length of element reduced.
        :Usage synchronize_until_element_disappear("[id*='RangeValuesBox']", 9)
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_obj = parent_object.find_element_by_css_selector(element_css).is_displayed()
            except NoSuchElementException:
                time.sleep(pause_time)
                temp_obj = False
            if temp_obj == False:
                run_=False
                break
            else:
                time.sleep(pause_time)
                continue
        time.sleep(pause_time)
    
    def synchronize_until_element_is_visible(self, element_css, expire_time, pause_time=1):
        '''
        This function is used to synchronize until element is visible.
        
        :Usage synchronize_until_element_disappear("[id*='RangeValuesBox']", 9)
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_obj = self.driver.find_element_by_css_selector(element_css).is_displayed()
            except NoSuchElementException:
                time.sleep(pause_time)
                temp_obj = False
            if temp_obj == True:
                run_=False
                break
            else:
                time.sleep(pause_time)
                continue
        time.sleep(pause_time)
    
    def synchronize_until_element_is_visible_within_parent_object(self, parent_object, element_css, expire_time, pause_time=1):
        '''
        This function is used to synchronize until element is visible.
        
        :Usage synchronize_until_element_disappear("[id*='RangeValuesBox']", 9)
        '''
        timeout=0
        run_ = True
        while run_:
            timeout+=1
            if timeout == int(expire_time)+1:
                raise ValueError('The Provided CSS - [ {0} ] for synchronization mismatched'.format(element_css))
            try:
                temp_obj = parent_object.find_element_by_css_selector(element_css).is_displayed()
            except NoSuchElementException:
                time.sleep(pause_time)
                temp_obj = False
            if temp_obj == True:
                run_=False
                break
            else:
                time.sleep(pause_time)
                continue
        time.sleep(pause_time)
    
    def wait_for_page_loads(self, time_out, sleep_interval=0.5, pause_time=1):
        """
        Webdriver will wait until complete the page load
        """
        JavaScript.wait_for_page_loads(self, time_out, sleep_interval, pause_time)
                
    def verify_element_color_using_get_attribute(self, element_css, color, msg, attribute='fill'):
        '''
        Desc : This function is to verify element color using element attribute.
        User can send css of the element, color name from color data and  message, parameter's values should be given when call the function
        '''
        if attribute == 'fill':
            if Global_variables.browser_name in ['ie', 'edge']:
                temp_obj=((self.driver.find_element_by_css_selector(element_css).get_attribute(attribute))[:-9]+")")[4:]
            else:
                temp_obj=((self.driver.find_element_by_css_selector(element_css).get_attribute(attribute))[:-10]+")")[4:]
            actual_color = "rgb"+temp_obj
            expected_color=UtillityMethods.color_picker(self, color, 'rgb')
        UtillityMethods.asequal(self, actual_color, expected_color, msg)
    
    def verify_element_color_using_css_property(self, element_css, color, msg, attribute='stroke', element_obj=None):
        '''
        Desc: This function is to verify element color using value of css property example 'stroke'
        '''
        if element_obj == None :
            actual_color = Color.from_string(self.driver.find_element_by_css_selector(element_css).value_of_css_property(attribute)).rgba
        else :
            actual_color = Color.from_string(element_obj.value_of_css_property(attribute)).rgba
        expected_color=UtillityMethods.color_picker(self, color, 'rgba')
        UtillityMethods.asequal(self, expected_color, actual_color, msg)
    
    def get_element_attribute(self, elem, attrib):
        '''
        Desc:- This function is to get a specified attribute value of an element.
        ''' 
        return(elem.get_attribute(attrib))
        
    def get_element_css_propery(self, elem, attrib):
        '''
        Desc:- This function is to get a specified attribute value of an element.
        ''' 
        return(elem.value_of_css_property(attrib))
    
    def verify_element_visiblty(self, element=None, element_css=None, visible=True, msg='Step X'):
        '''
        Desc:- This function is to verify whether the element is visible.
        '''
        try:
            if element!=None:
                status = element.is_displayed()
            elif element_css!=None:
                status = self.driver.find_element_by_css_selector(element_css).is_displayed()
        except NoSuchElementException:
            status = False
        UtillityMethods.asequal(self, status, visible, msg)
    
    def verify_element_disable(self, element=None, attribute_='class'):
        '''
        Desc:- This function is to verify whether the element is disabled.
        '''
        if element is None:
            raise AttributeError("Element is None.")
        try:
            element_class_value = UtillityMethods.get_element_attribute(self, element, attribute_)
            temp_value = element_class_value[0]
        except TypeError:
            del temp_value    
            raise TypeError("This element of '"+str(attribute_)+"' value is null.")
        status=bool(re.match('.*button-disabled', element_class_value))
        return (status)
        
    def as_List_equal(self,*params):
        Flag=False
        try:
            testobj = unittest.TestCase()
            testobj.assertListEqual(params[0], params[1], params[2])
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*(Step.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'List Equal comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)
    
    def asequal(self, *params):
        Flag=False
        try:
            testobj = unittest.TestCase()
            testobj.assertEqual(params[0], params[1], params[2])
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*([S|s]tep.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'Equal comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)
        
    def as_not_equal(self, *params):
        Flag=False
        try:
            testobj = unittest.TestCase()
            testobj.assertNotEqual(params[0], params[1], params[2])
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*(Step.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'Not Equal comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)
    
    def asin(self, *params):
        Flag=False
        try:
            #testobj = unittest.TestCase()
            assert params[0] in params[1], params[2]
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*(Step.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'ASIN comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)
            
    def as_notin(self, *params):
        Flag=False
        try:
            #testobj = unittest.TestCase()
            assert params[0] not in params[1], params[2]
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*(Step.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'Equal comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)
    
    def as_GE(self, *params):
        Flag=False
        try:
            testobj = unittest.TestCase()
            testobj.assertGreaterEqual(params[0], params[1], params[2])
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*(Step.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'As GEqual to comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)

    def as_LE(self, *params):
        Flag=False
        try:
            testobj = unittest.TestCase()
            testobj.assertLessEqual(params[0], params[1], params[2])
            print(params[2] + " - PASSED.")
            Global_variables.verification_steps.append(params[2] + " - PASSED.")
            Flag=True
        except AssertionError as e:
            m = re.match(r'.*(Step.*)...', str(e.args))
            msg = m.group(1)+" - FAILED."+'As LEqual to comparison : value1=['+str(params[0])+'], value2=['+str(params[1])+']'
            print(msg)
            Global_variables.verification_steps.append(msg)
            Global_variables.asert_failure_count += 1
            UtillityMethods.create_failure_log(self, msg)
        finally:
            suite_type=UtillityMethods.parseinitfile(self, 'suite_type')
            try:
                try:
                    step_number=re.search(r'\d+.\d+', params[2]).group()
                except AttributeError:
                    step_number=re.search(r'\d+', params[2]).group()
            except AttributeError:
                step_number=re.search(r'[x|X]', params[2]).group()
            if suite_type == 'smoke':
                file_name=Global_variables.current_test_case
                file_path=os.getcwd() + "\\" + file_name + "_" + step_number + ".png"
                self.driver.save_screenshot(file_path)
            else:
                pass
        UtillityMethods.verification_screenshot_capture(self, step_number, Flag)

    def verify_visible_elements(self, elements_obj, expected_total_visible_elements, msg):
        """
        Descriptions : This method used to get visible element count
        """
        actaul_visible_elements=0
        for element in elements_obj :
            if element.is_displayed() == True :
                actaul_visible_elements+=1
        UtillityMethods.asequal(self, expected_total_visible_elements, actaul_visible_elements, msg)

    def verify_placeholder(self, place_holder_css, place_holder_text, msg):
        """
        Description : This method it used to verify placeholder text value
        usage : verify_placeholder(".main-box", "30px", "Step 01.01 : verify placeholder value")
        """
        place_holder_obj = UtillityMethods.validate_and_get_webdriver_object(self, place_holder_css, "place holder css")
        actual_place_holder_value = place_holder_obj.get_attribute('placeholder')
        UtillityMethods.asequal(self, place_holder_text, actual_place_holder_value, msg)
        
    def verify_number_of_browser_windows(self, total_windows, step_num):
        """
        Descriptiion : Verify the number of browser windows
        :Usage - verify_number_of_browser_windows(2, '02.01')
        """
        total_windows = int(total_windows)
        actual_total_windows = len(self.driver.window_handles)
        msg = "Step {0} : Verify {1} windows opened in current browser".format(step_num, total_windows)
        UtillityMethods.asequal(self, total_windows, actual_total_windows, msg)
    
    def get_current_screen_specification(self):
        """
        This will return the specifications like height, width of the current monitor.
        :Usage browser_width, browser_height = CoreUtillityMethods.get_current_screen_specification(self)
        """
        dict_obj={}
        for _time in range(72):
            try:
                dict_obj['screen_width'] = self.driver.execute_script("return screen.width")
                dict_obj['screen_height'] = self.driver.execute_script("return screen.height")
                break
            except TimeoutException:
                time.sleep(5)
            except Exception as e:
                print("Exception occur in get_current_screen_specification- {0}".format(e))
        return (dict_obj)
    
    def get_current_browser_specification(self):
        """
        This will return the specifications like height, width of the actual working area of current focused browser.
        :Usage browser_width, browser_height = UtillityMethods.get_browser_height(self)
        """
        browser_specification_dict_obj={}
        if sys.platform == 'linux':
            browser_specification_dict_obj['browser_width']=self.driver.execute_script("return window.screenX")
            browser_screeny_=self.driver.execute_script("return window.screenY")
            outer_height = self.driver.execute_script("return window.outerHeight")
            inner_height = self.driver.execute_script("return window.innerHeight")
            browser_specification_dict_obj["browser_height"]=int(browser_screeny_ + (outer_height - inner_height))
        else:    
            screen_specification_dict_obj=UtillityMethods.get_current_screen_specification(self)
            for _time in range(72):
                try:
                    outer_height = self.driver.execute_script("return window.outerHeight;")
                    availWidth = self.driver.execute_script("return screen.availWidth;")
                    availHeight = self.driver.execute_script("return screen.availHeight;")
                    innerWidth = self.driver.execute_script("return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth || document.body.scrollWidth;")
                    scrollHeight=self.driver.execute_script("return document.body.scrollHeight || window.innerHeight;")
                    window_innerheight=self.driver.execute_script("return window.innerHeight || document.body.scrollHeight")
                    if scrollHeight > availHeight or scrollHeight < window_innerheight:
                        innerHeight = window_innerheight
                    else:
                        innerHeight = scrollHeight
                    break
                except TimeoutException:
                    time.sleep(5)
                except Exception as e:
                    print("Exception occur in get_current_browser_specification- {0}".format(e))
            browser_specification_dict_obj['browser_width'] = availWidth - innerWidth
            browser_specification_dict_obj['browser_height'] = availHeight - innerHeight
            browser_specification_dict_obj['outer_height'] = screen_specification_dict_obj['screen_height'] - outer_height
        return (browser_specification_dict_obj)
    
    def update_current_working_area_browser_specification(self):
        '''
        Desc:- This function will update current browser's 'browser_width' and 'browser_height' in the class variable 
        current_working_area_browser_width and current_working_area_browser_height. So when ever we move to any new page 
        we should call this function to keep update these two variables.
        '''
        browser_specification=UtillityMethods.get_current_browser_specification(self)
        Global_variables.current_working_area_browser_x=browser_specification['browser_width']
        Global_variables.current_working_area_browser_y=browser_specification['browser_height']
       
    def get_web_element_coordinate(self, web_element, element_location='middle', xoffset=0, yoffset=0):
        '''
        Desc:- This function will return the any web_object's screen x-y co-ordinate in a dictionary format.
        :param web_element:- the web element whose co-ordinate to be derived.
        :param element_location:- middle, top_left, top_middle, top_right, right_middle, bottom_right, bottom_middle, bottom_left, left_middle, left_top
        elem:- This is the object for which x,y coordinate to be returned.
        coordinate_type='start' OR 'top_middle' OR 'top_right' OR 'left' OR 'middle' OR 'right' OR 'bottom_left' OR 'bottom_middle' OR 'bottom_right' OR 'offset'
        The return type is a dictionary like = {'x': 524, 'y': 993}
        '''
        element_coordinate_dict_obj={}
        elem_x=web_element.location['x'] + Global_variables.current_working_area_browser_x
        elem_y=web_element.location['y'] + Global_variables.current_working_area_browser_y
        elem_h=web_element.size['height']
        elem_w=web_element.size['width']
        if element_location=='top_left':
            element_coordinate_dict_obj['x'] = elem_x + xoffset
            element_coordinate_dict_obj['y'] = elem_y + yoffset
        if element_location=='top_middle':
            element_coordinate_dict_obj['x'] = elem_x + (elem_w/2) + xoffset
            element_coordinate_dict_obj['y'] = elem_y + yoffset
        if element_location=='top_right':
            element_coordinate_dict_obj['x'] = elem_x + elem_w + xoffset
            element_coordinate_dict_obj['y'] = elem_y + yoffset
        if element_location=='middle_left':
            element_coordinate_dict_obj['x'] = elem_x + xoffset
            element_coordinate_dict_obj['y'] = elem_y + (elem_h/2) + yoffset
        if element_location=='middle':
            element_coordinate_dict_obj['x'] = elem_x + (elem_w/2) + xoffset
            element_coordinate_dict_obj['y'] = elem_y + (elem_h/2) + yoffset
        if element_location=='middle_right':
            element_coordinate_dict_obj['x'] = elem_x + elem_w + xoffset
            element_coordinate_dict_obj['y'] = elem_y + (elem_h/2) + yoffset
        if element_location=='bottom_left':
            element_coordinate_dict_obj['x'] = elem_x + xoffset
            element_coordinate_dict_obj['y'] = elem_y + elem_h + yoffset
        if element_location=='bottom_middle':
            element_coordinate_dict_obj['x'] = elem_x + (elem_w/2) + xoffset
            element_coordinate_dict_obj['y'] = elem_y + elem_h + yoffset
        if element_location=='bottom_right':
            element_coordinate_dict_obj['x'] = elem_x + elem_w + xoffset
            element_coordinate_dict_obj['y'] = elem_y + elem_h + yoffset
        return(element_coordinate_dict_obj)
    
    def switch_to_new_window(self, current_browser_window_title=None, window_maximize=True):
        '''
        Desc:- This function will switch the control from the current window to a specified window.
            After switching this will update the browser height, width and window handle list in the available class variable, so that they can be 
            used later. If browser equal to 'IE' and next_window_num is greater than '0' then update only browser height. It will handle IE browser crashed
            only in visualization section.
        :param window_num:- window number Starts with 1, 2, 3..
        :param current_browser_window_title:- current browser window title 
        '''
        UtillityMethods.switch_to_window(self)
        time.sleep(Global_variables.mediumwait)
        after_switch_window_widht = self.driver.execute_script("return window.innerWidth|| document.documentElement.clientWidth|| document.body.clientWidth;")
        if window_maximize == True:
            if after_switch_window_widht < self.driver.execute_script("return screen.availWidth;"):
                self.driver.maximize_window()
        time_count = 0
        while(after_switch_window_widht < self.driver.execute_script("return screen.availWidth;")):
            time_count+=1
            time.sleep(1)
            if time_count > 39:
                break
        time.sleep(Global_variables.shortwait)
        UtillityMethods.update_current_working_area_browser_specification(self)
        UtillityMethods.update_window_handles_list(self, update='add')
    
    def switch_to_previous_window(self, window_close=True):
        '''
        Desc:- This function will switch the control back to previous window by closing the current window.
        '''
        if window_close == True:
            self.driver.close()
        time.sleep(Global_variables.shortwait)
        UtillityMethods.update_window_handles_list(self, update='remove')
        self.driver.switch_to.window(Global_variables.windows_handles[-1])
        UtillityMethods.update_current_working_area_browser_specification(self)
    
    def switch_to_window(self):
        '''
        This function is used to switch from current working browser to specific browser window. 
        '''
        run_loop = True
        count_time=1
        while run_loop:
            if count_time == 90:
                raise TimeoutError('No new window found to switch.')
            if len(self.driver.window_handles) > len(Global_variables.windows_handles):
                run_loop = False
            count_time += 1
            time.sleep(1)
        old_windows=Global_variables.windows_handles
        new_windows=self.driver.window_handles
        new_set=set(new_windows)
        old_set=set(old_windows)
        diff_set=new_set-old_set
        last_window=list(diff_set)
        self.driver.switch_to.window(last_window[-1])
        
    def update_window_handles_list(self, update='add'):
        '''
        This Function will update the window handles and mantain the 'windows_handles' variable in init section.
        update='add' OR 'remove'
        ''' 
        if update=='add':
            Global_variables.windows_handles.append(self.driver.current_window_handle) 
        if update=='remove':
            unnecessary_window=Global_variables.windows_handles.pop() 
            del(unnecessary_window)
               
    def python_left_click(self, web_element, element_location='middle', xoffset=0, yoffset=0, mouse_move_duration=0.5):
        '''
        Desc:- This function will left click on the element using physical mouse cursor move.
        :param web_element 
        :param element_location:- middle
        :param xoffset:- 0, 20...
        :param yoffset:- 0, 20...
        :param mouse_move_duration:- 0.5, 1...
        '''
        (x, y)=UtillityMethods.python_move_to_element(self, web_element, element_location, xoffset, yoffset, mouse_move_duration)
        time.sleep(Global_variables.shortwait)
        if Global_variables.browser_name in ['ie', 'edge'] :
            uisoup.mouse.click(x, y)
        else :
            pyautogui.click(button='left')
    
    def python_right_click(self, web_element, element_location='middle', xoffset=0, yoffset=0, mouse_move_duration=0.5):
        '''
        Desc:- This function will right click on the element using physical mouse cursor move.
        :param web_element
        :param element_location:- middle
        :param xoffset:- 0, 20...
        :param yoffset:- 0, 20...
        :param mouse_move_duration:- 0.5, 1...
        '''
        (x, y)=UtillityMethods.python_move_to_element(self, web_element, element_location, xoffset, yoffset, mouse_move_duration)
        time.sleep(Global_variables.shortwait)
        if Global_variables.browser_name in ['ie', 'edge'] :
            uisoup.mouse.click(x, y, button_name=uisoup.mouse.RIGHT_BUTTON)
        else :
            pyautogui.click(button='right')
    
    def take_monitor_screenshot(self, file_name, image_type='actual', left=0, top=0, right=0, bottom=0):#Need to delete
        """
        :param file_name: file for saving
        :param image_type: where you want to save your image in directory
        :param left: how much you want to reduce the size from left in output of your image
        :param top: how much you want to reduce the size from top in output of your image
        :param right: how much you want to reduce the size from right in output of your image
        :param bottom: how much you want to reduce the size from bottom in output of your image
        :usage take_monitor_screenshot('full_monitor_screenshot', image_type='actual', left=10, top=25, right=10, bottom=25)
        """        
        if image_type=='actual' :
            location='actual_images'
        elif image_type=='fail' :
            location='failure_captures'
        else:
            location='images'
        file_path=os.getcwd() + "\\" + location + "\\" + file_name + ".png"
        im=ImageGrab.grab()
        im.save(file_path)
        resolution=pyautogui.size()
        left_rs = left
        top_rs = top
        right_rs=resolution[0]-right
        bottom_rs=resolution[1]-bottom
        bbox = (left_rs, top_rs, right_rs, bottom_rs)
        base_image = Image.open(file_path)
        cropped_image = base_image.crop(bbox)
        cropped_image.save(file_path)
        
    def verification_screenshot_capture(self, step_number, Flag):
        '''
        Description: This will capture screenshot and save it current working directory.
        Flag: Based on this argument test case name will go(Ex: if Flag is True, then case is C0011, Else Flag is Flase, then case is test_C0011)
        Usage : verification_screenshot_capture('09.01', True)
        '''
        case = Global_variables.current_test_case
        if not os.path.isdir(case):
            os.makedirs(case)
        case_id = case if Flag else 'test_'+str(case)
        file_name = case_id + '_' + step_number
        try:
            path_location = os.path.join(os.getcwd(),case)
            file_location = os.path.join(path_location, file_name + '.png')
            self.driver.save_screenshot(file_location)
            Global_variables.verification_test_case_name.append(file_name)
        except Exception as e:
            print(Exception(e))
            print('Exception in save screenshot of verification : ' + Global_variables.current_test_case)
            
    def list_values_verification(self, expected_list, acutal_list, step_num, values_name, assert_type, value_len=None, slicing=(None, None)):
        """
        Description: Verify the given list values with difference types of assert type.
        :Parameters:
            expected_list:list = List which contains expected values to verify.
            acutal_list:list = List which contains actual values to verify.
            step_num:str = Verification msg step number. Exmp: "03.01".
            values_name:str = Name of the values to compose verification message. Exmp: ContextMenu, X-Axisi Labels ans etc.
            assert_type:str: Method of assert. Exmp: "eqaul" , "notin", "in"
            value_len:int: Length of the list values. List should contains only string values.
            slicing:tuple: Slicing index values to slice given list before verify
        """
        assert_types = ("equal", "in", "notin")
        if assert_type not in assert_types:
            raise TypeError("[{}] is invalid assert type. Valid types are {}".format(assert_type, assert_types))
        acutal_list = acutal_list.copy()[slicing[0]:slicing[1]]
        if value_len:
            expected_list = [value[:value_len] for value in expected_list]
            acutal_list = [value[:value_len] for value in acutal_list]
        if assert_type == assert_types[0]:
            msg = "Step {0} : Verify {1}".format(step_num, values_name)
            self.as_List_equal(expected_list, acutal_list, msg)
        elif assert_type == assert_types[1]:
            missing_values = set(expected_list) - set(acutal_list)
            msg = "Step {0} : Verify {1} in {2}".format(step_num, expected_list, values_name)
            if len(expected_list) == 0:
                self.asin(expected_list, acutal_list, msg)
            elif missing_values:
                self.asin(list(missing_values), acutal_list, msg)
            else:
                self.asequal(True, True, msg)
        elif assert_type == assert_types[2]:
            msg = "Step {0} : Verify {1} not in {2}".format(step_num, expected_list, values_name)
            not_missing_values = set(expected_list).intersection(acutal_list)
            if not_missing_values:
                self.asin(list(not_missing_values), acutal_list, msg)
            else:
                self.asequal(True, True, msg)
        else:
            raise NotImplemented
        
    def color_picker(self, color, rgb_type='rgb'):
        """
        Usage: color_picker(self,'comment', 'rgba')
        params:color='green'
        params:rgb_type='rgb' or 'rgba' or 'transparent'
        return:rgb(0, 0, 0) or rgba(0, 0, 0)
        """
        color_file=os.path.join(root_path.ROOT_PATH, 'color.data')
        section = 'transparent' if color == 'transparent' else 'DEFAULT'
        color_pair = {}
        parser = ConfigParser()
        parser.optionxform=str
        parser.read(color_file)
        try:
            color_pair[color] = parser[section][color]
            if rgb_type=='rgb':
                return (rgb_type + color_pair[color])
            elif rgb_type=='transparent':
                return(color_pair[color])
            else:
                return(rgb_type + re.sub('\)', ', 1)', color_pair[color]))
        except (KeyError, NoOptionError) as e:
            print("Specified Color is not available in color.data. " + str(e))
            return
        
    def create_failure_log(self, msg):
        try:
            Global_variables.verification_failure_msg_list.append(msg)
        except:
            print("Unable to append in failure capture message '{0}' to verification_failure_msg_list",format(msg))
 
    
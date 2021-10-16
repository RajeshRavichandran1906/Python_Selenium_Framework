class Global_variables :
    
    current_time=None
    browser_name=None
    current_working_area_browser_x = 0
    current_working_area_browser_y = 0
    asert_failure_count=0
    ie_crash_wndnum=1
    windows_handles=[]
    shortwait = 1
    mediumwait = 3
    longwait = 5
    verification_failure_msg_list=[]
    current_test_case=None
    saved_case_flag=False
    test_case_name_to_log = []
    testrail_steps_doc = []
    verification_test_case_name = [] 
    verification_steps=[]
    used_username_in_current_session = {}
    webdriver = None
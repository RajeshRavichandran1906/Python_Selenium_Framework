import time
from os.path import os
from datetime import datetime
from selenium import webdriver
from configparser import ConfigParser
from common.lib.configfiles import settings
from common.lib.utillity import UtillityMethods

class DriverLauncher(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def execute(self):
        configFile = 'config.ini'
        parser = ConfigParser()
        parser.read(os.path.join(settings.CONFIG_ROOT, configFile))              
        section = 'firefox'
        option = 'executables_path'
        targetPath = parser[section][option]
        option = 'executable'
        firefoxTargetExec = parser[section][option]
        targetExec = targetPath + firefoxTargetExec
        option = 'download_preference'
        download_pref = parser.getboolean(section,option)
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.useDownloadDir", download_pref)
        i=0
        while i<5:
            start = time.time()
            now = datetime.now()
            Start_time = now.strftime("%H:%M:%S")
            try:
                print("Start Time =", Start_time)
                return webdriver.Firefox(firefox_profile=profile, executable_path=targetExec)
            except Exception as e:
                UtillityMethods.kill_browser_process(self)
                i += 1
                print("Number of attempts to load gecko driver: ", i)
                print("Exception Raised is:")
                print("_"*20)
                print(e)
                print("_"*20)
                now = datetime.now()
                End_time = now.strftime("%H:%M:%S")
                print("End Time =", End_time)
                end = time.time()
                print("Elapsed Time :", (end - start))
                continue
            else:
                break
        
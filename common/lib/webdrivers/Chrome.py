from os.path import os
from selenium import webdriver
from configparser import ConfigParser
from common.lib.configfiles import settings


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
        section = 'chrome'      
        option = 'executables_path'
        targetPath = parser[section][option]    
        option = 'executable'
        chromeTargetExec = parser[section][option]
        targetExec = targetPath + r'\\' + chromeTargetExec
        options = webdriver.ChromeOptions()
        prefs = {"download.prompt_for_download": bool(parser[section]['prompt_for_download'])}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        opts=parser[section]['argument'].split(',')
        for opt in opts:
            options.add_argument(opt)
        return webdriver.Chrome(executable_path=targetExec, chrome_options=options)
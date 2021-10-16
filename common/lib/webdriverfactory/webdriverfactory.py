import inspect
import importlib
from os.path import os
import common.lib.configfiles.settings
from configparser import ConfigParser, NoOptionError

class WebDriverFactory:
    
    """Web driver factory using command objects"""
    configFile = 'config.ini'
    defaultErrorMessage = 'The config file ' + configFile + ' for the WebDriverFactory is corrupted.'

    @classmethod
    def getInstance(cls, browserName):  

        unsupportedBrowserMessage, missingBrowserMessage = cls.__getErrorMessages()  
        unsupportedBrowserMessage = unsupportedBrowserMessage +  ' [ ' + browserName + ' ] '             
        if (browserName == None):
            raise ValueError(missingBrowserMessage)              
        try:
            browserName = browserName.lower()
        except AttributeError:
            raise ValueError(unsupportedBrowserMessage)    
        driverFactoryModules = cls.__getSupportedDriverLaunchers()     
        if browserName in driverFactoryModules:
            return driverFactoryModules[browserName].execute() 
        else:
            raise ValueError(unsupportedBrowserMessage) 
         
    @classmethod
    def __getModulesList(cls): 
        parser = ConfigParser()
        parser.read(os.path.join(common.lib.configfiles.settings.CONFIG_ROOT, cls.configFile))  
              
        section = 'supported_browsers' 
        if not parser.has_section(section):
            raise ResourceWarning(cls.defaultErrorMessage) 
        return set(parser.options(section)) - set(parser.defaults())

    @classmethod
    def __getLauncherInstance(cls, nameToImport, launcherClassName): 
        try:            
            theModule = importlib.import_module(nameToImport)
            for currentValue in theModule.__dict__.values():
                if inspect.isclass(currentValue) and (currentValue.__name__ == launcherClassName):
                    return currentValue()
        except ImportError:
            pass
        msg = cls.defaultErrorMessage + ' ' + nameToImport + ' ' + launcherClassName
        raise  ResourceWarning(msg)
                                                
    @classmethod
    def __getSupportedDriverLaunchers(cls): 
        driverFactoryModules = dict()     
        modulesList = cls.__getModulesList()  
        parser = ConfigParser()
        parser.read(os.path.join(common.lib.configfiles.settings.CONFIG_ROOT, cls.configFile))        
        section = 'supported_browsers' 
        classNameOption = 'launcher_class_name' 

        for option in modulesList:
            launcherClassName = parser[section][classNameOption]
            nameToImport = parser[section]['launcher_package'] + '.' + parser[section][option] 
            driverFactoryModules[option] = cls.__getLauncherInstance(nameToImport, launcherClassName)

        return driverFactoryModules
   
    @classmethod
    def __getErrorMessages(cls): 
        parser = ConfigParser()
        parser.read(os.path.join(common.lib.configfiles.settings.CONFIG_ROOT, cls.configFile))          
        section = 'error_messages' 
        try:
            option = 'unsupported'            
            unsupportedBrowserMessage = parser[section][option]  
            option = 'missing'
            missingBrowserMessage = parser[section][option]  
        except (KeyError, NoOptionError) :
            raise ResourceWarning(cls.defaultErrorMessage)  
        return unsupportedBrowserMessage, missingBrowserMessage
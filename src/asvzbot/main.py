# Import from Python standard library
import os
import argparse

# Import self-made additions
from log import *

# Import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService # Brave
from selenium.webdriver.firefox.service import Service as FirefoxService # Mozilla Firefox
from selenium.webdriver.chrome.service import Service as ChromiumService # Chromium
from selenium.webdriver.chrome.service import Service as ChromeService # Google Chrome
from selenium.webdriver.edge.service import Service as EdgeService # Microsoft Edge

# Import Selenium Errors
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import SessionNotCreatedException
#WebDriverException
#ModuleNotFoundError

# Import Webdriver
from webdriver_manager.chrome import ChromeDriverManager # Google Chrome, Chromium and Brave
from webdriver_manager.firefox import GeckoDriverManager # Mozilla Firefox
from webdriver_manager.microsoft import EdgeChromiumDriverManager # Microsoft Edge
from webdriver_manager.core.utils import ChromeType # Additionally needed for Chromium and Brave

# Configurations
HEADLESS = True # Set this to false if you want to see Selenium do its magic visibly
BROWSER_SELECTION = ["brave", "chromium", "chrome", "firefox", "edge"]
BRAVE_INSTALLATION_PATH = os.path.expandvars(r'%PROGRAMFILES%/BraveSoftware/Brave-Browser/Application/brave.exe')

def getDriver(browser=False):
    '''
    Create instance of desired browser. If no parameter is given, ASVZ-BOT automatically determines a browser to use.
    '''

    # Create web driver options
    match browser:
        case "brave":
            options = webdriver.ChromeOptions()
            options.binary_location = BRAVE_INSTALLATION_PATH # In contrary to the other browsers, the location of the browser executable must must be provided
        case "chromium":
            options = webdriver.ChromeOptions()
        case "chrome":
            options = webdriver.ChromeOptions()
        case "firefox":
             options = webdriver.FirefoxOptions()
        case "edge":
             options = webdriver.EdgeOptions()
    
    # Assign arguments to web driver options
    if browser in ["brave", "chromium", "chrome", "edge"]:
        # Find all Firefox options here: https://wiki.mozilla.org/Firefox/CommandLineOptions
        options.add_argument("--incognito")
        options.add_argument('--disable-translate')
        options.add_argument("--log-level=0") # From which level should error messages appear: INFO = 0,  WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
        options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disable "DevTools listening (...)"
        options.add_experimental_option("prefs", {"intl.accept_languages": "de"})
    else:
        options.add_argument("-private")
    options.headless = HEADLESS

    # Create new instance of web driver (Display error with type and message if driver was not created successfully)
    logger.info(browser[0].upper() + browser[1:] + " instance creation initiated")
    match browser:
        case "brave":
            try: driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=options)
            except (WebDriverException, SessionNotCreatedException) as err: logger.error(str(type(err)) + " " + str(err).split("\n")[0])
        case "chromium":
            try: driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
            except (WebDriverException, SessionNotCreatedException) as err: logger.error(str(type(err)) + " " + str(err).split("\n")[0])
        case "chrome":
            try: driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            except (WebDriverException, SessionNotCreatedException) as err: logger.error(str(type(err)) + " " + str(err).split("\n")[0])
        case "firefox":
            try: driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            except (WebDriverException, SessionNotCreatedException) as err: logger.error(str(type(err)) + " " + str(err).split("\n")[0])
        case "edge":
            try: driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            except (WebDriverException, SessionNotCreatedException) as err: logger.error(str(type(err)) + " " + str(err).split("\n")[0])

    # Test if 'driver' has been created, meaning a new instance has been created successfully
    try: driver
    except: return False
    else:
        logger.info(browser[0].upper() + browser[1:] + " instance successfully created")
        return driver

def main():

    # Clear the console before each new run
    os.system('cls' if os.name == 'nt' else 'clear')

    # Initiate parser
    parser = argparse.ArgumentParser("Parser")

    # Configure command-line argument parser (argument is followed by variable)
    parser.add_argument("-u", "--username", type=str, help="provide the username you use to login to ASVZ")
    parser.add_argument("-p", "--password", type=str, help="provide the password to the corresponding username")
    parser.add_argument("-b", "--browser", type=str, help="provide if you want to use a specific browser", choices=BROWSER_SELECTION)

    # Configure command-line argument parser (argument has meaning by just providing it)
    parser.add_argument("--switchaai", help="add if you login with SWITCH AAI", action="store_true")
    parser.add_argument("--asvzid", help="add if you login with ASVZ ID", action="store_true")

    # Convert all arguments (unused ones too) into an 'Namespace' object, from which the arguments can be accessed programmatically
    args = parser.parse_args()

    # Check that only either SWITCH AAI or ASVZ ID is set
    if args.switchaai and args.asvzid: 
        logger.error("Provide only one login method: Either pass '--switchaai' or '--asvzid' as an argument, depending on your ASVZ login method. Do not pass both.")
        return
    if not args.switchaai and not args.asvzid: 
        logger.error("Provide a valid login method: Either pass '--switchaai' or '--asvzid' as an argument, depending on your ASVZ login method.")
        return

    # Create new browser instance (if a specific browser has been provided)
    driver = False
    if not args.browser is None:
        driver = getDriver(args.browser)
    
    # getDriver() returns 'False' if no driver could be created, so this if-statement triggers when the desired browser fails or none has been tested yet
    if driver == False:
        for browser in BROWSER_SELECTION:
            driver = getDriver(browser)
            if not driver == False: break
    
    # If still no browser could be found, the user does not have a compatible browser installed
    if driver == False:
        logger.error("No compatible browser could be found. Please install a supported browser: " + str(BROWSER_SELECTION)[1:-1])
        return

    # Get sample website and print it's HTML source
    driver.get("https://api.perytron.ch/ARES.php?x=10000&y=10000")
    driver.implicitly_wait(3)
    print (driver.page_source.encode("utf-8"))

    # Quit and close browser
    driver.quit()
    logger.info("Browser instance successfully quit. Bye, have a great time!")

# The main() function is only called if this module ("main.py") has been run directly.
if __name__ == "__main__":
    main()
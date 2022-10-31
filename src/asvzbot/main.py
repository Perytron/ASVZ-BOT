# Import from Python standard library
import os
import argparse

# Import self-made additions
from log import *

# Import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Import Selenium Errors
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import SessionNotCreatedException
#WebDriverException
#ModuleNotFoundError

# Import Webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Browser Installation Paths
BRAVE_INSTALLATION_PATH = os.path.expandvars(r'%PROGRAMFILES%/BraveSoftware/Brave-Browser/Application/brave.exe')

def main():

    # Clear the console before each new run
    os.system('cls' if os.name == 'nt' else 'clear')

    # Initiate parser
    parser = argparse.ArgumentParser("Parser")

    # Configure parser
    parser.add_argument("--switchaai", help="add if you login with SWITCH AAI", action="store_true")
    parser.add_argument("--asvzid", help="add if you login with ASVZ ID", action="store_true")
    parser.add_argument("-u", "--username", type=str, help="provide the username you use to login to ASVZ")
    parser.add_argument("-p", "--password", type=str, help="provide the password to the corresponding username")

    # Convert all arguments (unused ones too) into an 'Namespace' object, from which the arguments can be accessed programmatically
    args = parser.parse_args()

    # Check that only either SWITCH AAI or ASVZ ID is set
    if args.switchaai and args.asvzid: 
        logger.error("Provide only one login method: Either pass '--switchaai' or '--asvzid' as an argument, depending on your ASVZ login method. Do not pass both.")
        return
    if not args.switchaai and not args.asvzid: 
        logger.error("Provide a valid login method: Either pass '--switchaai' or '--asvzid' as an argument, depending on your ASVZ login method.")
        return

    # Web driver options
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito") # Called "--private" on Firefox
    options.add_argument("--headless") # Comment out this option if you want to see Selenium do its magic visibly
    options.add_argument('--disable-translate')
    options.add_argument("--log-level=0") # From which level should error messages appear: INFO = 0,  WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disable "DevTools listening (...)"
    options.add_experimental_option("prefs", {"intl.accept_languages": "de"})
    options.binary_location = BRAVE_INSTALLATION_PATH

    # Create new instance of web driver
    logger.info("Browser instance creation initiated")
    try: driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Display error with type and message if driver was not created successfully
    except (WebDriverException, SessionNotCreatedException) as err: logger.error(type(err), str(err).split("\n")[0])
    logger.info("Browser instance successfully created")

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
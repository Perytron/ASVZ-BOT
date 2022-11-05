# Import from Python standard library
import os
import argparse
import json
from pathlib import Path

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
LOGIN_SELECTION = ["asvz", "switch"]
BRAVE_INSTALLATION_PATH = os.path.expandvars(r'%PROGRAMFILES%/BraveSoftware/Brave-Browser/Application/brave.exe')
CONFIGURATION_FILE = "config.json"

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
        options.add_argument("--log-level=3") # From which level should error messages appear: INFO = 0,  WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
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

def getConfiguration(arguments, filename):
    '''
    Collect necessary configuration either from the configuration file, the command-line arguments or a combination of both and return a dictionary
    '''

    configuration_requirements = ["username", "password", "browser", "login", "id"] # List holding the options which are required for the script to function properly
    configuration_collected = {} # Dictionary holding the extracted configuration which will be returned to the script after this functions ends
    arguments_dictionary = {} # Dictionary holding the converted command-line arguments
    configuration_json = {} # Dictionary holding the extracted configuration from 'config.json'

    # Convert the required arguments into a dictionary for easy access later on
    for key in configuration_requirements:
        try: 
            argument_value = getattr(arguments, key)
            if not argument_value is None: arguments_dictionary[key] = argument_value
        except: continue

    # Check that the configuration file exists
    if Path(filename).is_file():

        # Read the configuration file and parse its JSON content to a new dictionary
        with open(filename, "r") as file: 
            try:
                configuration_json = json.load(file)
            except: 
                logger.error("There was an error parsing '" +  filename + "'. Please either fix or delete the file.")
                return False
            
        # Loop over the newly created JSON dictionary and extract the useful configuration
        for key in configuration_json.keys():
            if key in configuration_requirements:

                # Check validity of input (it could be that user manually edits 'config.json')
                match key:
                    case "browser":
                        if not configuration_json[key] in BROWSER_SELECTION: 
                            logger.warning("Provided browser is invalid. Pick one of the following options: " + str(', '.join(BROWSER_SELECTION)))
                            continue
                    case "login":
                        if not configuration_json[key] in LOGIN_SELECTION: 
                            logger.warning("Provided login method is invalid. Pick one of the following options: " + str(', '.join(LOGIN_SELECTION)))
                            continue

                configuration_collected[key] = configuration_json[key]
    
    # Loop over all command-line arguments and extract the useful configuration (overrides JSON because command-line is regarded as priority)
    for key in arguments_dictionary.keys(): configuration_collected[key] = arguments_dictionary[key]

    # Make sure that in the end every requirement has been provided (on either way: command-line arguments or 'config.json')
    if not sorted(configuration_collected.keys()) == sorted(configuration_requirements):
        difference = set(configuration_requirements) - set(configuration_collected.keys()) # Retrieve elements that should be extracted but were not found on either way
        logger.error("You have forgot to feed ASVZ-bot with the following value(s): " + str(', '.join(difference)))
        return False
    
    # Store the configuration in the JSON file for later usage (don't store password if '-s' / '--stealth' has been provided)
    with open(filename, "w") as file:
        output_directory = configuration_collected.copy()
        if arguments.stealth: del output_directory["password"]
        json.dump(output_directory, file, sort_keys=True, indent=4)
        
    return configuration_collected


def main():

    # Clear the console before each new run
    os.system('cls' if os.name == 'nt' else 'clear')

    # Initiate parser
    parser = argparse.ArgumentParser("Parser")

    # Configure command-line argument parser (argument is followed by variable)
    parser.add_argument("-u", "--username", type=str, help="provide username you use to login to ASVZ")
    parser.add_argument("-p", "--password", type=str, help="provide password to the corresponding username")
    parser.add_argument("-b", "--browser", type=str, help="provide if you want to use a specific browser", choices=BROWSER_SELECTION)
    parser.add_argument("-l", "--login", type=str, help="provide login method", choices=LOGIN_SELECTION)
    parser.add_argument("-i", "--id", type=int, help="provide sports lesson id")

    # Configure command-line argument parser (argument has meaning by just providing it)
    parser.add_argument("-s", "--stealth", help="do not store the password in 'config.json'", action="store_true")

    # Convert all arguments (unused ones too) into an 'Namespace' object, from which the arguments can be accessed programmatically
    arguments = parser.parse_args()

    # Collect configurations from either the configuration file, the command-line options or a combination of both
    configuration = getConfiguration(arguments, CONFIGURATION_FILE)

    # If the configuration could not retreive all reqired values, exit the script
    if not configuration: return

    # Create new browser instance
    driver = getDriver(configuration["browser"])
    
    # getDriver() returns 'False' if no driver could be created, so this if-statement triggers when the desired browser fails or none has been tested yet
    if not driver:
        for browser in BROWSER_SELECTION:
            driver = getDriver(browser)
            if not driver == False: break
    
    # If still no browser could be found, the user does not have a compatible browser installed
    if not driver:
        logger.error("No compatible browser could be found. Please install a supported browser: " + str(BROWSER_SELECTION)[1:-1])
        return

    # Get sample website and print its HTML source
    driver.get("https://api.perytron.ch/ARES.php?x=10000&y=10000")
    driver.implicitly_wait(3)
    print (driver.page_source.encode("utf-8"))

    # Quit and close browser
    driver.quit()
    logger.info("Browser instance successfully quit. Bye, have a great time!")

# The main() function is only called if this module ("main.py") has been run directly.
if __name__ == "__main__":
    main()
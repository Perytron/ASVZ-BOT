from os import path

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
BRAVE_INSTALLATION_PATH = path.expandvars(r'%PROGRAMFILES%/BraveSoftware/Brave-Browser/Application/brave.exe')

# Web driver options
options = webdriver.ChromeOptions()
options.add_argument("--incognito") # called "--private" on Firefox
options.add_argument("--headless") # Comment out this option if you want to see Selenium do its magic visibly
options.add_argument('--disable-translate')
options.add_experimental_option("prefs", {"intl.accept_languages": "de"})
options.binary_location = BRAVE_INSTALLATION_PATH

# Create new instance of web driver
try: driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Display error with type and message if driver was not created successfully
except (WebDriverException, SessionNotCreatedException) as err: print(type(err), str(err).split("\n")[0])

# Get sample website and print it's HTML source
driver.get("https://api.perytron.ch/ARES.php?x=10000&y=10000")
driver.implicitly_wait(3)
print (driver.page_source.encode("utf-8"))

# Quit and close browser
driver.quit()
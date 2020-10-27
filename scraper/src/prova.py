import time

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--verbose')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return options


time.sleep(2)
driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',
                          options=set_chrome_options())
driver.get('https://en.wikipedia.org/wiki/A.C._Milan')
print(driver.find_element_by_class_name("firstHeading").text)
# Do stuff with your driver
driver.close()

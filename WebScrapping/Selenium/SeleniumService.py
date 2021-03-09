from time import sleep
from typing import Union
import platform

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver


class SeleniumService:
    AVAILABLE_DRIVERS = ['chrome', 'firefox']

    def __init__(self, headless=False, driver='chrome', options=None, start=True):
        assert driver in self.AVAILABLE_DRIVERS
        self.headless = headless
        self.driver_type = driver
        self.options: Union[webdriver.ChromeOptions, webdriver.FirefoxOptions, None] = options
        self.driver: Union[webdriver.Chrome, webdriver.Firefox, None] = None
        if start:
            self.start()

    def start(self):
        assert self.driver_type in self.AVAILABLE_DRIVERS
        if self.driver_type == 'chrome':
            self.start_chrome()
        elif self.driver_type == 'firefox':
            self.start_firefox()

    def start_chrome(self):
        self.driver = webdriver.Chrome(
            options=self.options if self.options else self.generate_chrome_options(),
            executable_path=self.get_executable('chromedriver'),
        )
        self.driver_type = 'chrome'

    def start_firefox(self):
        fp = webdriver.FirefoxProfile('automation/user-data/firefox')
        self.driver = webdriver.Firefox(
            options=self.options if self.options else self.generate_firefox_options(),
            executable_path=self.get_executable('geckodriver'),
            firefox_profile=fp
        )
        self.driver_type = 'firefox'

    def get_executable(self, driver):

        sysname = platform.system()

        if sysname == "Darwin":
            return f'WebScrapping/Selenium/drivers/mac/{driver}'
        elif sysname == "Linux":
            return f'automation/src/linux/{driver}'
        elif sysname == "Windows":
            return f'WebScrapping/Selenium/drivers/windows/{driver}.exe'
        else:
            raise ValueError(f"OS name is incorrect: {sysname}")

    def generate_chrome_options(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument('--lang=en_US')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--enable-precise-memory-info")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-default-apps")
        self.options.headless = True if self.headless else False
        return self.options

    def generate_firefox_options(self):
        self.options = webdriver.FirefoxOptions()
        self.options.headless = True if self.headless else False
        return self.options

    def wait(self, sec):
        return WebDriverWait(self.driver, sec)

    def sleep(self, sec):
        sleep(sec)

    @property
    def achain(self):
        return ActionChains(self.driver)

    def stop(self):
        self.driver.quit()

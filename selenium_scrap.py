# import undetected_chromedriver as uc
# uc.TARGET_VERSION = 85
# uc.install(executable_path="chromedriver.exe")
from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
import sys
import time
import random


data = {"Name": [],
        "Internet": [],
        "E-mail": [],
        "Telefon": [],
        "Adresse": [],
        "PLZ": [],
        "Mitarbaiter": [],
        "Branche": [],
        "Link": []
        }
df = pd.DataFrame(data, columns=["Name", "Internet", "E-mail", "Telefon",
                                 "Adresse", "PLZ", "Mitarbaiter", "Branche", "Link"])

DRIVER_PATH = 'chromedriver.exe'
# PROXY = "95.174.67.50:18080"
# chrome_options.add_argument("--headless")
# webdriver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
options = Options()
options.add_argument("--user-data-dir=automation/user-data/chrome")
# self.options.add_argument("--user-data-dir=/Users/vash/Library/Application Support/Google/Chrome")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--enable-precise-memory-info")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-default-apps")
# options.add_argument('--proxy-server=%s' % PROXY)


# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(
    options=options,
    executable_path=DRIVER_PATH,

)

driver_type = 'chrome'


pages = []
driver.get("http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php")
time.sleep(random.randint(4, 10))
javaScript = "window.scrollBy(0,300);"
driver.execute_script(javaScript)
time.sleep(random.randint(4, 10))
# page = driver.page_source
# soup = BeautifulSoup(page, 'html.parser')
for i in range(1, 7):
    if i % 6 == 0:
        driver.execute_script(javaScript)
    try:
        link = driver.find_element_by_css_selector(f"#firmen > ul.list-group > li:nth-child({i}) > a")
        first_click = link.click()
        time.sleep(random.uniform(4, 10))
        driver.execute_script(f"window.scrollBy(0, 300)")
        time.sleep(random.uniform(4, 10))

        # page = driver.page_source
        # soup = BeautifulSoup(page)
        # pages.append(soup)
        driver.execute_script("window.history.go(-1)")
        time.sleep(random.uniform(4, 10))
    except Exception as e:
        print(e)
        continue
# driver.quit()

# lis = soup.find_all(class_="list-group")
# temp = "http://www.firmendb.de"
#
# links = {}
# for i in lis:
#
#     children = i.find_all("a", recursive=True)
#     for child in children:
#         links[child.text] = temp + child.attrs["href"][2:]




# for k, v in links.items():
#     driver.get(v)
#     pg = driver.page_source
#     sp = BeautifulSoup(pg, "html.parser")
#     pages.append(sp)
#     time.sleep(random.uniform(4, 10)
# )



# driver.get('http://www.firmendb.de/firmen/7496035.php')
# pg = driver.page_source
# sp = BeautifulSoup(pg, "html.parser")
# name = sp.find("span", itemprop="name")
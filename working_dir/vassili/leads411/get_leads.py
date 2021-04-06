from WebScrapping.Selenium.SeleniumService import SeleniumService
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from json.decoder import JSONDecodeError
scrapper = SeleniumService()


def get_js_script(start):
    return """
    
    var req = await fetch("https://app2.lead411.com/getMoreSearchResults", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,et;q=0.6,en-US;q=0.5",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": "masWNT98GAFdYjsKKSLGOQqU6gIvFTsz6Bm8n4hx",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://app2.lead411.com/searchpage/49919",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "display_start=%%%START%%%&search_data%5Bzip%5D=&search_data%5Brange%5D=5&search_data%5Bstate%5D=&search_data%5Btitle%5D=&search_data%5Buser_search_string%5D=&search_data%5Bsic%5D=&search_data%5Btechnology%5D=&search_data%5BsoftwareHardware%5D=&search_data%5BareaCode%5D=&search_data%5BemployeeSkills%5D=&search_data%5BindustryCode%5D=&search_data%5BFilterRevenue%5D=all%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12&search_data%5BFilterEmployee%5D=all%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12&search_data%5BFilterLevel%5D%5B%5D=c_level&search_data%5BFilterLevel%5D%5B%5D=vp_level&search_data%5BFilterLevel%5D%5B%5D=director_level&search_data%5BFilterLevel%5D%5B%5D=manager_level&search_data%5BFilterType%5D=resultTypeAll%2CcompanyResultsAll%2CpeopleResultsEmails%2CresultNormal%2C%2CempSizeAsc%2Csuppressed_no%2C%2Clinkedin_no%2C2021-03-06%2CUS%2Cexported_no%2Chas_direct_dial_no%2C%2Chas_mobile_dial_no%2C%2C&search_data%5BPress_event_data%5D=%232021-04-06%232021-04-06&search_data%5Bcompany_description_string%5D=&search_data%5Btitle_keyword%5D=&search_data%5Bproduct_keyword%5D=&search_data%5Bkeyword_match_text%5D=&search_data%5Btechnology_uses_text%5D=&search_data%5Bexact_widenet_value%5D=exact&search_data%5Bzip_location_for%5D=zip_location_company&search_data%5Bper_company_match%5D=all&search_data%5BAdvancePeopleFilterFieldsData%5D=%7B%22hasPatent%22%3A%22no%22%2C%22has_patent_keyword%22%3A%22%22%2C%22hasCertification%22%3A%22no%22%2C%22has_certification_keyword%22%3A%22%22%2C%22hasAward%22%3A%22no%22%2C%22has_award_keyword%22%3A%22%22%2C%22schoolAlumin%22%3A%22%22%2C%22fluentLanguages%22%3A%22%22%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

res = await req.json()
return res
""".replace("%%%START%%%", start)



scrapper.driver.get('https://app.dnbhoovers.com/login')

scrapper.driver.find_element_by_id('username').send_keys('info@cordellandsonenterprises.com')
scrapper.driver.find_element_by_css_selector("button[type='submit'][tabindex='3']").click()
scrapper.driver.find_element_by_id('password').send_keys('Northface14!')
scrapper.driver.find_element_by_css_selector("button[type='submit'][tabindex='2']").click()
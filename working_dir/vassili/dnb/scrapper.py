from WebScrapping.Selenium.SeleniumService import SeleniumService
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from json.decoder import JSONDecodeError
scrapper = SeleniumService()


def get_js_script(start):
    return """a = await fetch("https://app.dnbhoovers.com/api/search", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "hpk": "1615145549275-%s",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://app.dnbhoovers.com/search/company",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": JSON.stringify({"query":"","searchWeight":0,"filters":[{"employeesThisSiteRangesFacet":{"ranges":[{"from":1}]}}],"aggs":{},"from":%s,"size":25,"sortBy":[{"company":[{"numEmployees_l":"desc"}]}],"types":["company"]}),
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});

b = await a.json()
return b
""" % (start, start)


scrapper.driver.set_script_timeout(60)

scrapper.driver.get('https://app.dnbhoovers.com/login')

scrapper.driver.find_element_by_id('username').send_keys('info@cordellandsonenterprises.com')
scrapper.driver.find_element_by_css_selector("button[type='submit'][tabindex='3']").click()
scrapper.driver.find_element_by_id('password').send_keys('Northface14!')
scrapper.driver.find_element_by_css_selector("button[type='submit'][tabindex='2']").click()

bounds = [0.060, 0.061]
count = 21150
for i in range(1000):

    bounds = [round(i+0.001, 3) for i in bounds]

    for k in range(400):
        count += 1
        print('Scraping', count)

        try:
            scrapper.wait(10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='next-pg paginator-arrow-right']" ))).click()
            # scrapper.driver.find_element_by_css_selector("div[class='next-pg paginator-arrow-right']").click()
            # scrapper.sleep(1)
            scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
            scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))

            reqs = scrapper.driver.requests[-30:]
            reqs.reverse()
            for rr in reqs:
                if 'https://app.dnbhoovers.com/api/search' == rr.url:
                    aa = json.loads(rr.response.body)['searchResults']['results']
                    with open(f"working_dir/vassili/dnb/data/data_{count}.json", "w") as f:
                        json.dump(aa, f)
                    break
        except TimeoutException as e:
            print("Request timeout")
            continue
        except JSONDecodeError as e:
            print("JSONDecodeError")
            continue

    scrapper.driver.find_element_by_css_selector("input[placeholder='From'][data-qa-id='salesRangesFacet-from']").send_keys(str(bounds[0]))
    scrapper.driver.find_element_by_css_selector("input[placeholder='To'][data-qa-id='salesRangesFacet-to']").send_keys(str(bounds[1]))
    scrapper.driver.find_element_by_css_selector("button[data-qa-id='salesRangesFacet-btn']").click()
    scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.driver.find_elements_by_css_selector("a[class='js-remove-value search-control-selected-value-remove']")[1].click()
    scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))

    scrapper.driver.find_element_by_css_selector("input[name='page-num']").send_keys('1')
    scrapper.driver.find_element_by_css_selector("input[name='page-num']").send_keys(Keys.ENTER)
    scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))




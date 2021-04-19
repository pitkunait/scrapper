from WebScrapping.Selenium.SeleniumService import SeleniumService
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from json.decoder import JSONDecodeError
scrapper = SeleniumService()



def get_js_script(start):
    return """aa = await fetch("https://app.dnbhoovers.com/api/contact/email/%s", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
  },
  "referrer": "https://app.dnbhoovers.com/search/saved/9bb2e96c-b40a-4413-82e7-f247d13ce9b2",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});

b = await aa.json()
return b
""" % start


scrapper.driver.set_script_timeout(50)

scrapper.driver.get('https://app.dnbhoovers.com/login')

scrapper.driver.find_element_by_id('username').send_keys('info@cordellandsonenterprises.com')
scrapper.driver.find_element_by_css_selector("button[type='submit'][tabindex='3']").click()
scrapper.driver.find_element_by_id('password').send_keys('Northface14!')
scrapper.driver.find_element_by_css_selector("button[type='submit'][tabindex='2']").click()

bounds = [1, 2]
count = 0
for i in range(1000):

    bounds = [i+1 for i in bounds]
    try:
        pagess = scrapper.wait(20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='page-last page-link']")))
        ranfee = int(pagess.text)
        if ranfee > 400:
            ranfee = 400
    except Exception as e:
        ranfee = 400

    for k in range(ranfee):
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
                    with open(f"working_dir/vassili/dnb/emails/data/data_{count}.json", "w") as f:
                        json.dump(aa, f)


                    for bb in aa:
                        idd = bb.get('id')
                        try:
                            if idd:
                                email = scrapper.driver.execute_script(get_js_script(idd))
                                email['id'] = idd
                                with open(f"working_dir/vassili/dnb/emails/emails/email_{idd}.json", "w") as f:
                                    json.dump(email, f)
                        except Exception:
                            print('Error', idd)


                    break
        except TimeoutException as e:
            print("Request timeout")
            continue
        except JSONDecodeError as e:
            print("JSONDecodeError")
            continue

    scrapper.driver.find_element_by_css_selector("input[placeholder='From'][data-qa-id='employeesThisSiteRangesFacet-from']").send_keys(str(bounds[0]))
    scrapper.driver.find_element_by_css_selector("input[placeholder='To'][data-qa-id='employeesThisSiteRangesFacet-to']").send_keys(str(bounds[1]))
    scrapper.driver.find_element_by_css_selector("button[data-qa-id='employeesThisSiteRangesFacet-btn']").click()
    scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.driver.find_elements_by_css_selector("a[class='js-remove-value search-control-selected-value-remove']")[1].click()
    scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))

    scrapper.driver.find_element_by_css_selector("input[name='page-num']").send_keys('1')
    scrapper.driver.find_element_by_css_selector("input[name='page-num']").send_keys(Keys.ENTER)
    scrapper.wait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))
    scrapper.wait(360).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='loading-overlay']")))




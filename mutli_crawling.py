import threading
import time
import concurrent.futures
import pandas as pd
from proxycrawl.proxycrawl_api import ProxyCrawlAPI
from bs4 import BeautifulSoup
import re


re_telefon = re.compile("Telefon")
re_email = re.compile("Email")
re_internet = re.compile("Internet")
re_arbaiter = re.compile('Mitarbaiter')
re_branche = re.compile('Branche')

class MultiThreading:
    def __init__(self):
        self.df = pd.DataFrame(columns=["Name", "Internet", "E-mail", "Telefon", "Adresse", "PLZ", "Mitarbaiter", "Branche", "Link"])
        self._lock = threading.Lock()
        self.api = ProxyCrawlAPI({'token': 'QllJvSA8-qu2DOOdroaj0w'})
        self.links = {}
        self.list = []
        self.sps = []
        self.erlst = []

    def generate_url(self, n):
        if n == 0:
            return "http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php"
        else:
            return f"http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck_{n}.php"


    def get_links(self, link):
        try:
            response = self.api.get(link, {'page_wait': 5000})
            print(response)
            if response['status_code'] == 200:
                print(response['body'])
            soup = BeautifulSoup(response["body"])
            temp = "http://www.firmendb.de"
            lis = soup.find_all(class_="list-group")
            for i in lis:
                children = i.find_all("a", recursive=True)
                for child in children:
                    self.links[child.text] = temp + child.attrs["href"][2:]
        except Exception as e:
            self.erlst.append(e)
            print(e)

    def add_to_df(self):
        for i in self.list:
            self.df = self.df.append(i, ignore_index=True)

    def get_data(self, k, v):
        start_time = time.time()

        r = self.api.get(v, {'page_wait': 5000})

        obj = {}

        if r['status_code'] == 200:
            print(r['status_code'])
            sp = BeautifulSoup(r["body"], from_encoding="UTF-8")
            base = sp.find("dl", class_="dl-horizontal dl-short dl-antiblock nomargin-bottom")
            add = sp.find("dl", class_="dl-horizontal dl-antiblock")
            self.sps.append(add)
            try:
                name = base.find("span", itemprop="name").text
                obj['Name'] = name
                street = base.find("span", itemprop="streetAddress").text
                obj["Adresse"] = street
                postal = base.find("span", itemprop="postalCode").text
                city = base.find("span", itemprop="addressLocality").text
                obj['PLZ'] = postal + " " + city
            except Exception as e:
                obj['Name'] = ""
                obj["Adresse"] = ""
                obj['PLZ'] = ""
                print(e)
            try:
                telefon = base.find("dt", text=re_telefon).find_next("dd").contents[0]
                obj["Telefon"] = telefon
            except Exception as e:
                obj["Telefon"] = ""
                print(e)
            try:
                email = base.find("dt", text=re_email).find_next("dd").contents[0].text
                obj['E-mail'] = email
            except Exception as e:
                obj['E-mail'] = ""
                print(e)
            try:
                internet = base.find("dt", text=re_internet).find_next("dd").contents[0].text
                obj['Internet'] = internet
            except Exception as e:
                obj['Internet'] = ""
                print(e)
            try:
                workers = add.find("span", itemprop="numberOfEmployees").text
                obj["Mitarbaiter"] = workers
            except Exception as e:
                obj["Mitarbaiter"] = ""
                print(e)
            try:
                branch = add.find("dt", text=re_branche).find_next("dd").contents[0].text
                obj["Branche"] = branch
            except Exception as e:
                obj["Branche"] = ""
                print(e)
            obj["Link"] = v
            elapsed_time = time.time() - start_time
            print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
            self.list.append(obj)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for k, v in self.links.items():
                executor.submit(self.get_data, k, v)

    def scrap_all(self):
        for i in range(8, 115):
            self.get_links(self.generate_url(i))
            self.run()
        self.add_to_df()
        return self.df


a = MultiThreading()
df = a.scrap_all()

# a.df.to_excel("automation\sample_data.xlsx")
# dx.to_excel("automation\partial_data_Osnabrueck.xlsx")
dxx = pd.DataFrame(a.list)
dxx.to_excel("automation\partial_data_Osnabrueck_1.xlsx")
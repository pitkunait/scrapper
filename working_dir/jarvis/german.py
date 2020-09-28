import logging
import pickle
import re

import pandas as pd
from bs4 import BeautifulSoup

from WebScrapping.ProxyCrawler import ProxyCrawler

logging.basicConfig(level=logging.DEBUG)

re_telefon = re.compile("Telefon")
re_email = re.compile("Email")
re_internet = re.compile("Internet")
re_arbaiter = re.compile('Mitarbaiter')
re_branche = re.compile('Branche')


class GermanCrawling:

    def __init__(self):
        self.df = pd.DataFrame(
            columns=["Name", "Internet", "E-mail", "Telefon", "Adresse", "PLZ", "Mitarbaiter", "Branche", "Link"])
        self.list_200 = []
        self.dict_200 = {}
        self.list_errors = []
        self.list = []
        self.sps = []
        self.erlst = []
        self.crawler = ProxyCrawler()

        self.crawler.options.BAD_PROXY_PATH = 'working_dir/jarvis/bad_proxies.pickle'
        self.crawler.retrieve_bad_proxies()
        self.crawler.add_proxies()
        self.retrieve_200_dict()

    @staticmethod
    def generate_url(n):
        if n == 0:
            return "http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php"
        else:
            return f"http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck_{n}.php"

    def check_200_validity(self, request):
        if request.status_code != 200:
            return False

        sp = BeautifulSoup(request.content, from_encoding="UTF-8")
        if sp.find("is using a security service for protection against"
                   " online attacks. This process is automatic. You will be"
                   " redirected once the validation is complete."):
            return False

        return True

    def get_links_data(self):
        self.crawler.add_proxies()
        for i in range(116):
            url = self.generate_url(i)
            if url in self.dict_200:
                continue
            resp = self.crawler.get(url, test_function=self.check_200_validity)
            self.list_200.append(resp)
            self.dict_200[url] = resp.content

    def parse_company_links(self, content):
        temp = "http://www.firmendb.de"
        links = {}
        soup = BeautifulSoup(content, parser="html")
        lis = soup.find_all(class_="list-group")
        for k in lis:
            children = k.find_all("a", recursive=True)
            for child in children:
                links[child.text] = temp + child.attrs["href"][2:]
        return links

    def parse_company_data(self, v):
        obj = {}
        sp = BeautifulSoup(v, from_encoding="UTF-8")
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
        self.list.append(obj)

    def add_to_200_dict(self):
        for i in self.list_200:
            self.dict_200[i.url] = i.content

    def dump_200_dict(self):
        with open("working_dir/jarvis/status200.pickle", 'wb') as f:
            pickle.dump(self.dict_200, f)

    def retrieve_200_dict(self):
        try:
            with open("working_dir/jarvis/status200.pickle", 'rb') as f:
                dict_200 = pickle.load(f)
                if len(dict_200) > 0:
                    self.dict_200 = dict_200
        except Exception as e:
            print(e)

    def check_existing_200_responses(self):
        mutable_dict = self.dict_200.copy()
        for i, k in self.dict_200.items():
            if not self.check_200_validity(k):
                mutable_dict.pop(i)


if __name__ == '__main__':
    crawler = GermanCrawling()
    crawler.get_links_data()

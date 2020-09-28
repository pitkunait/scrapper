import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from itertools import cycle
from requests.exceptions import ProxyError, TooManyRedirects
from ProxyCrawler.ProxyParser import ProxyParser
import pickle


re_telefon = re.compile("Telefon")
re_email = re.compile("Email")
re_internet = re.compile("Internet")
re_arbaiter = re.compile('Mitarbaiter')
re_branche = re.compile('Branche')


class ProxyCrawler:

    def __init__(self, retrieve_bad_proxies=True, retrieve_200_responces=True):
        self.proxy_set = set()
        self.bad_proxies = []
        self.proxy_pool = cycle(self.proxy_set)
        self.df = pd.DataFrame(columns=["Name", "Internet", "E-mail", "Telefon", "Adresse", "PLZ", "Mitarbaiter", "Branche", "Link"])
        self.list_200 = []
        self.dict_200 = {}
        self.list_errors = []
        self.list = []
        self.sps = []
        self.erlst = []
        self.proxy_parser = ProxyParser()

        if retrieve_bad_proxies:
            self.retrieve_shit_proxies()

        if retrieve_200_responces:
            self.retrieve_200_dict()

    def save_results(self):
        self.dump_200_dict()
        self.dump_shit_proxies()

    @staticmethod
    def generate_url(n):
        if n == 0:
            return "http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php"
        else:
            return f"http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck_{n}.php"

    def dump_shit_proxies(self):
        with open("bad_proxies.pickle", 'wb') as f:
            pickle.dump(self.bad_proxies, f)

    def retrieve_shit_proxies(self):
        try:
            with open("bad_proxies.pickle", 'rb') as f:
                bad_proxies = pickle.load(f)
                if len(bad_proxies) > 0:
                    self.bad_proxies = bad_proxies
        except Exception as e:
            print(e)

    def dump_200_dict(self):
        with open("status200.pickle", 'wb') as f:
            pickle.dump(self.dict_200, f)

    def retrieve_200_dict(self):
        try:
            with open("status200.pickle", 'rb') as f:
                dict_200 = pickle.load(f)
                if len(dict_200) > 0:
                    self.dict_200 = dict_200
        except Exception as e:
            print(e)

    def test_runner(self):
        self.add_proxies()
        for i in range(116):

            url = self.generate_url(i)

            if url in self.dict_200:
                continue

            self.check_proxies(url)

    def check_proxies(self, url):

        def remove_and_restart(self, url, proxy):
            print("Removing", proxy, ". proxies left:", len(self.proxy_set))
            self.remove_proxy(proxy)
            self.check_proxies(url)

        proxy = next(self.proxy_pool)
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response.status_code, url)
            if response.status_code == 200:
                if self.check_200_validity(response.content):
                    self.list_200.append(response)
                    self.dict_200[url] = response.content
                else:
                    remove_and_restart(self, url, proxy)
            else:
                self.list_errors.append(response)
                remove_and_restart(self, url, proxy)

        except (ProxyError, TooManyRedirects):
            remove_and_restart(self, url, proxy)

    def check_200_validity(self, content):
        sp = BeautifulSoup(content, from_encoding="UTF-8")
        if sp.find("is using a security service for protection against"
                   " online attacks. This process is automatic. You will be"
                   " redirected once the validation is complete."):
            return False
        return True

    def check_existing_200_responses(self):
        mutable_dict = self.dict_200.copy()
        for i, k in self.dict_200.items():
            if not self.check_200_validity(k):
                mutable_dict.pop(i)

    def remove_proxy(self, to_delete):
        self.proxy_set.remove(to_delete)
        self.bad_proxies.append(to_delete)
        self.proxy_pool = cycle(self.proxy_set)

    def add_proxies(self):
        new_proxies = self.proxy_parser.get_all_proxies()
        for i in new_proxies:
            if i not in self.bad_proxies:
                self.proxy_set.add(i)
        self.proxy_set = self.proxy_parser.get_all_proxies()
        self.proxy_pool = cycle(self.proxy_set)

    def add_to_200_dict(self):
        for i in self.list_200:
            self.dict_200[i.url] = i.content

    def jarik_1(self, url, proxy):

        temp = "http://www.firmendb.de"
        links = {}

        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response)
            soup = BeautifulSoup(response.content, parser="html")
            lis = soup.find_all(class_="list-group")
            for k in lis:
                children = k.find_all("a", recursive=True)
                for child in children:
                    links[child.text] = temp + child.attrs["href"][2:]
        except Exception:
            print("Skipping. Connnection error")

    def parse_data(self, v):
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


crawler = ProxyCrawler()


url = crawler.generate_url(10)
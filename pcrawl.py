from proxycrawl.proxycrawl_api import ProxyCrawlAPI
from bs4 import BeautifulSoup
import requests
from time import sleep
import json
import pandas as pd
import re
import time
import threading

api = ProxyCrawlAPI({'token': 'QllJvSA8-qu2DOOdroaj0w'})


def generate_url(n):
    if n == 0:
        return "http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php"
    else:
        return f"http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck_{n}.php"

# for i in range(115):
# response = api.get(generate_url(i), {'page_wait': 5000})
# if response['status_code'] == 200:
#     print(response['body'])

response = api.get('http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php', {'page_wait': 5000})
if response['status_code'] == 200:
    print(response['body'])

soup = BeautifulSoup(response["body"])

temp = "http://www.firmendb.de"

links = {}

lis = soup.find_all(class_="list-group")

for i in lis:

    children = i.find_all("a", recursive=True)
    for child in children:
        links[child.text] = temp + child.attrs["href"][2:]

df = pd.DataFrame(columns=["Name", "Internet", "E-mail", "Telefon",
                                 "Adresse", "PLZ", "Mitarbaiter", "Branche", "Link"])

start_time = time.time()


def get_data():
    for k, v in links.items():
        r = api.get(v, {'page_wait': 5000})
        row = len(df)
        if r['status_code'] == 200:
            print(r['status_code'])
            sp = BeautifulSoup(r["body"])
            base = sp.find("dl", class_="dl-horizontal dl-short dl-antiblock nomargin-bottom")
            add = sp.find("dl", class_="dl-horizontal dl-antiblock")
            try:
                name = base.find("span", itemprop="name").text
                df.loc[row, 'Name'] = name
                street = base.find("span", itemprop="streetAddress").text
                df.loc[row, "Adresse"] = street
                postal = base.find("span", itemprop="postalCode").text
                city = base.find("span", itemprop="addressLocality").text
                df.loc[row, 'PLZ'] = postal + " " + city
            except Exception as e:
                df.loc[row, 'Name'] = ""
                df.loc[row, "Adresse"] = ""
                df.loc[row, 'PLZ'] = ""
                print(e)
            try:
                telefon = base.find("dt", text=re.compile("Telefon")).find_next("dd").contents[0]
                df.loc[row, "Telefon"] = telefon
            except Exception as e:
                df.loc[row, "Telefon"] = ""
                print(e)
            try:
                email = base.find("dt", text=re.compile("Email")).find_next("dd").contents[0]
                df.loc[row, 'E-mail'] = email
            except Exception as e:
                df.loc[row, 'E-mail'] = ""
                print(e)
            try:
                internet = base.find("dt", text=re.compile("Internet")).find_next("dd").contents[0].text
                df.loc[row, 'Internet'] = internet
            except Exception as e:
                df.loc[row, 'Internet'] = ""
                print(e)
            try:
                workers = add.find("dt", text=re.compile('Mitarbaiter')).find_next("dd").contents[0].text
                df.loc[row, "Mitarbaiter"] = workers
            except Exception as e:
                df.loc[row, "Mitarbaiter"] = ""
                print(e)
            try:
                branch = add.find("dt", text=re.compile('Branche')).find_next("dd").contents[0].text
                df.loc[row, "Branche"] = branch
            except Exception as e:
                df.loc[row, "Branche"] = ""
                print(e)
            df["Link"] = v
            elapsed_time = time.time() - start_time
            print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
            print(len(df))

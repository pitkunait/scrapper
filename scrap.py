import pandas as pd
import cfscrape as cf
from bs4 import BeautifulSoup
import requests
from time import sleep


temp = "http://www.firmendb.de"

links = {}

x = cf.create_scraper()



def generate_url(n):
    if n == 0:
        return "http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck.php"
    else:
        return f"http://www.firmendb.de/deutschland/Niedersachsen_Osnabrueck_{n}.php"


for k in range(41):
# for k in range(3):
    sleep(2)
    url = generate_url(k)
    print(url)
    pg = x.get(url).content

    soup = BeautifulSoup(pg, 'html.parser')

    lis = soup.find_all(class_="list-group")

    for i in lis:

        children = i.find_all("a", recursive=True)
        for child in children:
            links[child.text] = temp + child.attrs["href"][2:]


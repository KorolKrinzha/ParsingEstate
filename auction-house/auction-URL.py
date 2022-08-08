import requests
import json
from bs4 import BeautifulSoup

url = "https://auction-house.ru/sitemap.xml"
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
url_info = soup.find_all('url')
for location in url_info:
    try:
        link = location.find('loc')
        link_string = link.string
        try:
            link_object = link_string.split('/')[3]
            if link_object =='catalog':print(link_string.string)
        except:
            continue
        
    except:
        continue

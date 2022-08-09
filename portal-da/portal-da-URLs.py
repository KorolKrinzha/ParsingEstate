import requests
import json
from bs4 import BeautifulSoup

url = "https://portal-da.ru/sitemap.xml"
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
url_info = soup.find_all('url')
for location in url_info:
    try:
        link = location.find('loc')
        print(link.string)
    except:
        continue
import requests
import json
from bs4 import BeautifulSoup
import os
from SingleSite import parsePage


# для отслеживания прогресса
from progressbar import ProgressBar
pbar = ProgressBar()

# ID проекта
auction_id = 'b3387693b4df4207996722578e301581'

if not os.path.exists('./result'):
    os.makedirs('./result')

url = "https://auction-house.ru/sitemap.xml"
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
url_info = soup.find_all('url')
for location in pbar(url_info):
    try:
        link = location.find('loc')
        link_string = link.string
        try:
            link_object = link_string.split('/')[3]
            if link_object =='catalog':
                auction_object_link = link_string.string
                parsePage(auction_object_link, auction_id)
        except:
            continue
        
    except:
        continue

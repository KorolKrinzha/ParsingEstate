import requests
import json
from bs4 import BeautifulSoup
import os
from SingleSite import parsePage


# для отслеживания прогресса
from progressbar import ProgressBar
pbar = ProgressBar()

# ID проекта
kf_id = '3b1fa59f0f814f93a5d04c3fcd0f53f7'

if not os.path.exists('./result'):
    os.makedirs('./result')

for page in pbar(range(1,96)):
    url = f"https://kf.expert/gorod/search?page={page}&pay_type_ids=1&separ_group_id=r_gorod&currency_alias=rur&prices_key_prefix=sale_from_all&county_ids=126&county_ids=559&county_ids=561&county_ids=573&county_ids=656&county_ids=709"
    page = requests.get(url)  


    soup = BeautifulSoup(page.content, "html.parser")

    for link in soup.find_all('a',  class_=  "card__gallery-wrapper"):
        kf_object_link = link.get('href')
        parsePage(kf_object_link, kf_id)
    continue
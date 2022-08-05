import requests
import json
from bs4 import BeautifulSoup


for page in range(1,96):
    url = f"https://kf.expert/gorod/search?page={page}&pay_type_ids=1&separ_group_id=r_gorod&currency_alias=rur&prices_key_prefix=sale_from_all&county_ids=126&county_ids=559&county_ids=561&county_ids=573&county_ids=656&county_ids=709"
    page = requests.get(url)  # This page outputs the HTML code of the page.


    soup = BeautifulSoup(page.content, "html.parser")

    for link in soup.find_all('a',  class_=  "card__gallery-wrapper"):
        print(link.get('href'))
# print(soup.title)

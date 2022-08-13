import requests
import json
from bs4 import BeautifulSoup

url = "https://investmoscow.ru/sitemap.tenders.xml"
exist_checker_url = "https://api.investmoscow.ru/investmoscow/tender/v1/object-info/getTenderObjectInformation?tenderId="
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
url_info = soup.find_all('url')
for location in url_info:
    try:
        link = location.find('loc')
        link_string = link.string
        try:
            link_object = link_string.split('/')[3]
            if link_object =='tenders':
                link_string = link_string.string
                id_start = link_string.find('=')
                tender_id = link_string[id_start+1:]
                exist_checker = requests.get(exist_checker_url+tender_id)
                
                if exist_checker.status_code==200:
                    invest_object_link = 'https://investmoscow.ru/tenders/tender/'+tender_id
                    print(invest_object_link)
            
        except:
            continue
        
    except:
        continue

import requests
import json
from bs4 import BeautifulSoup
from uuid import uuid4
import os
from SingleSite import parsePage # функция для парсинга страницы

# для отслеживания прогресса
from progressbar import ProgressBar
pbar = ProgressBar()


# ID проекта
osob_id = '80e9f2287fc74a39af7e551b30f34124'


# создаем папку куда суем результаты
if not os.path.exists('./result'):
    os.makedirs('./result')

osob_object_data = {
    "id":"",
    "resource":  {
    "title":"osobnyaki",
    "link":"",
    },
"realEstate": {
    "title":"",
    "description":"",
    "totalPrice":"",
    "area":""
},
"address":{
    "country":"",
    "region":"",
    "metro":""
},
"photo_link": [
    
]    
}

osob_object_geo = {
    "id": "",
    "latitude": "",
    "longitude": ""
}

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)
    for site in pbar (data):
        # записываем id каждого объекта
        site_id = str(uuid4())
        site_id = site_id.replace('-', "")
        osob_object_data['id'] = f'{osob_id}_{site_id}'
        
        filename = site['alias']
        # Ссылка на ресурс - домена+/+alias
        osob_object_link = 'https://osobnyaki.com/'+filename
        osob_object_data['resource']['link'] = osob_object_link
        
        # pagetitle - описание место где находится особняк
        osob_object_data['realEstate']['title'] = "Особняк "+ site['pagetitle']
        osob_object_data['address']['country'] = 'Россия'
        osob_object_data['address']['region'] =  site['pagetitle']
        

        # в values содержится геолокация в формате широта,долгота 
        osob_object_geo['id'] = f'{osob_id}_{site_id}'
        osob_object_geo['latitude'] = site['value'].split(',')[0]
        osob_object_geo['longitude'] = site['value'].split(',')[1]
        
        with open(f'./result/GEO_{filename}.json', 'w', encoding='utf-8') as fp:
            json_data = json.dumps(
                    osob_object_geo, ensure_ascii=False, indent=4)
            fp.write(json_data)

        with open(f'./result/{filename}.json', 'w', encoding='utf-8') as fp:
            json_data = json.dumps(
                osob_object_data, ensure_ascii=False, indent=4)
            fp.write(json_data) 
            
        parsePage(osob_object_link, filename)

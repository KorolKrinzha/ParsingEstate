import requests
import json
from bs4 import BeautifulSoup, Comment
import os
from uuid import uuid4

trust_object_data = {
    "id":"",
    "resource":  {
        
    "title":"trust",
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
    "city":"",
    "region":"",
    "street": ""
},
"photo_link": [
    
]    
}

trust_object_geo = {
    "id": "",
    "latitude": "",
    "longitude": ""
}
# Уже были найдены
# - цена
# - название
# - адрес
def parsePage( trust_object_data, trust_id):
    trust_object_link = trust_object_data['resource']['link']
    # ID 
    site_id = str(uuid4())
    site_id = site_id.replace('-', "")
    trust_object_data['id'] = f'{trust_id}_{site_id}'
    # ИМЯ ФАЙЛА
    if trust_object_link[-1] != "/": trust_object_link+='/'
    filename = trust_object_link.split('/')[-2]
    
    url = trust_object_link
    page = requests.get(url)
    
    if page.status_code==404: return
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    # ОПИСАНИЕ
    div_description = soup.find('div', attrs={"class":"text text--big"} ) # первый div с таким классом - описание
    try:
        description = div_description.contents[0] 
        description = " ".join(description.split()) # избавляемся от лишних пробелов 
        trust_object_data['realEstate']['description'] = description
    except: pass
    
    # ПЛОЩАДЬ
    description_items = soup.find_all('li', attrs={"class":"list__item"})
    try:
        for description_item in description_items:
            if 'м²' in description_item.contents[0]:
                area = description_item.contents[0]
                area = " ".join(area.split())
                trust_object_data['realEstate']['area'] = area
                break
    except Exception as e: pass 
    
    # КАРТИНКИ
    images_list = soup.find_all('img', attrs={'class':'card-slider__image'})
    try:
        for image in images_list:
            photo_link = 'https://www.trust.ru'+str(image['src'])  
            trust_object_data['photo_link'].append(photo_link) 
    except: pass
    
    
    with open(f'./result/{filename}.json', 'w', encoding='utf-8') as fp:
        # записываем в json_data значения основного json
        json_data = json.dumps(
            trust_object_data, ensure_ascii=False, indent=4)
        fp.write(json_data)
    

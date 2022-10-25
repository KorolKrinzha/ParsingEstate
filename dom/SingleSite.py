import requests
import json
from bs4 import BeautifulSoup, Comment
import os
from uuid import uuid4

dom_object_data = {
    "id":"",
    "resource":  {
        
    "title":"dom",
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
    "region":""

},
"photo_link": [
    
]    
}

dom_object_geo = {
    "id": "",
    "latitude": "",
    "longitude": ""
}

def parsePage(dom_object_link,dom_id):
    dom_object_data['id'] = dom_id
    dom_object_data['resource']['link'] = dom_object_link
    site_id = str(uuid4())
    site_id = site_id.replace('-', "")
    dom_object_data['id'] = f'{dom_id}_{site_id}'
    # имя файла 
    if dom_object_link[-1] != "/": dom_object_link+='/'
    filename = dom_object_link.split('/')[-2][4:]
    # имя файла это по сути айди аукциона
    page = requests.get(dom_object_link)
    
    if page.status_code==404: 
        return
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Проверяем, архивный ли лот
    title_tag = soup.find("meta", attrs={"property": "og:title"})
    if 'Архив' in str(title_tag) or 'архив' in str(title_tag): 
        return
    
    
    # НАЗВАНИЕ
    div_title = soup.find("div", attrs={"class":"page-heading__title page-title"})
    try:
        # Регион и нзвание совпадают
        dom_object_data['realEstate']['title'] =  str(div_title.contents[0])
        dom_object_data['address']['country'] =  'Россия'
        dom_object_data['address']['region'] =  str(div_title.contents[0])
    except: pass
    
    # ОПИСАНИЕ
    div_description = soup.find("div", attrs={"class":"auction-additional-info__text"})
    try:
        dom_object_data['realEstate']['description'] = str(div_description.contents[0])
    except: pass
    
    
    # ЦЕНА
    # ПЛОЩАДЬ

    a_price_tag = soup.find_all('div', attrs={"class":"auction-info__value auction-info__value_big"})
    # на сайте всего дважды встречаются div с данным классом. Сначала с ценой, затем с площадью 
    try:
        dom_object_data['realEstate']['totalPrice'] = str(a_price_tag[0].contents[0])
    except: pass
    try: 
        dom_object_data['realEstate']['area'] = str(a_price_tag[1].contents[0])
    except: pass

    # КАРТИНКИ
    picture_tag = soup.find('slider-with-thumbs')
    try:
        for picture in picture_tag[':data'].strip('[]').split(","):
            picture = picture.replace("\\", '').replace(']','').replace('[', '').replace('"','').replace("'","")
            picture = 'https://xn--d1aqf.xn--p1ai'+picture
            dom_object_data['photo_link'].append(picture)
    except Exception as e: print(e)
    
    
    # ГЕОЛОКАЦИЯ
    object_location = soup.find('object-location')
    try:
        # бывает такое, что локации и не бывает. Если нет, не будем записывать файл с геолокацией
        if object_location!=None:
            
            latitude = object_location['data'].strip('[]').split(",")[1][7:-1]
            longitude = object_location['data'].strip('[]').split(",")[2][7:-1]
            dom_object_geo['latitude'] = latitude
            dom_object_geo['longitude'] = longitude
            dom_object_geo['id'] = f'{dom_id}_{site_id}'
            
            with open(f'./result/GEO_{filename}.json', 'w', encoding='utf-8') as fp:
                # записываем в json_data значения основного json
                json_data = json.dumps(
                    dom_object_geo, ensure_ascii=False, indent=4)
                fp.write(json_data)
                        
    except Exception as e: print(e)
    
    
    
    
    
    

    
    
    with open(f'./result/{filename}.json', 'w', encoding='utf-8') as fp:
        # записываем в json_data значения основного json
        json_data = json.dumps(
            dom_object_data, ensure_ascii=False, indent=4)
        fp.write(json_data)


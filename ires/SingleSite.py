import requests
import json
from bs4 import BeautifulSoup, Comment
import os
from uuid import uuid4

ires_object_data = {
    "id":"",
    "resource":  {
        
    "title":"ires",
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

ires_object_geo = {
    "id": "",
    "latitude": "",
    "longitude": ""
}

def parsePage(ires_object_link,ires_id):
    ires_object_data['id'] = ires_id
    ires_object_data['resource']['link'] = ires_object_link
    site_id = str(uuid4())
    site_id = site_id.replace('-', "")
    ires_object_data['id'] = f'{ires_id}_{site_id}'
    # имя файла 
    if ires_object_link[-1] != "/": ires_object_link+='/'
    filename = ires_object_link.split('/')[-2]
    
    url = ires_object_link
    page = requests.get(url)
    
    if page.status_code==404: return
    
    soup = BeautifulSoup(page.content, "html.parser")


    # НАЗВАНИЕ
    title_tag = soup.find("meta", attrs={"property": "og:title"})
    # "Продажа / Производственный цех / Московская область" ---> "Производственный цех"
    title_tag = title_tag['content'].split("/")[1].strip()
    ires_object_data['realEstate']['title'] = str(title_tag)
    
    
    p_list = soup.find_all("p")
    for i in range(len(p_list)):
        # ОПИСАНИЕ
        try:
            if p_list[i]['class']==['h2'] and p_list[i].contents==['Описание']:
                # после параграфа с надписью "Описание" идет описание 
                # поэтому мы ищем описание среди всех параграфов, пока не найдем флаг
                description = p_list[i+1].contents[0]
                ires_object_data['realEstate']['description'] = str(description)
        except Exception as e:
            pass
        
        # АДРЕС
        try:
            # в параграфе с strong надписью "Расположение:" есть данные об областях
            if p_list[i].find('strong')!=None:
                if p_list[i].find('strong').contents==['Расположение:']:
                    # область
                    region = p_list[i].find('a').contents[0]
                    ires_object_data['address']['country'] = "Россия"
                    ires_object_data['address']['region'] = str(region)
        except: pass
        
        # ПЛОЩАДЬ
        try:
            if p_list[i]['class']==['tb15'] and p_list[i].contents==['Площадь']:
                
                # после надписи Площадь идет площадь
                ires_object_data['realEstate']['area'] = str(p_list[i+1].contents[0])
                
        except Exception as e: pass
        
        # ЦЕНА
        try:
            if p_list[i]['class']==['oiprice']:
                # на сайте еще есть span с долларами и евро, но нас интересует пока рубли
                rubles = p_list[i].find('span', attrs={"id":'prub'})
                if rubles !=None: 
                    ires_object_data['realEstate']['totalPrice'] = rubles.contents[0].strip()
                
                
        except Exception as e: pass
                
    # ПИКЧИ
    img_list = soup.find_all('img')
    for img in img_list:
        try:
            if 'ires-group.ru' in img['src'] and 'uploads' in img['src'] and 'logo' not in img['src']:
                image = img['src']
                ires_object_data['photo_link'].append(image)
        except: pass
    
    # ГЕОЛОКАЦИЯ
    a_geo_list = soup.find_all('a')
    for a in a_geo_list:
        try:
            coordinates = a['data-coords']
            ires_object_geo['id'] = f'{ires_id}_{site_id}'
            # дана строка, убираем по краям скобки
            coordinates = coordinates.replace('[','').replace(']','')
            # сначала широта, потом долгота
            ires_object_geo['latitude'] = coordinates.split(',')[0]
            ires_object_geo['longitude'] = coordinates.split(',')[1]
            
            break
        except Exception as e: pass
        
    with open(f'./result/GEO_{filename}.json', 'w', encoding='utf-8') as fp:
        json_data = json.dumps(
                ires_object_geo, ensure_ascii=False, indent=4)
        fp.write(json_data)

    with open(f'./result/{filename}.json', 'w', encoding='utf-8') as fp:
        # записываем в json_data значения основного json
        json_data = json.dumps(
            ires_object_data, ensure_ascii=False, indent=4)
        fp.write(json_data)

        
    

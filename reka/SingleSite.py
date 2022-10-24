import requests
import json
from bs4 import BeautifulSoup, Comment
import os
from uuid import uuid4

reka_object_data = {
    "id":"",
    "resource":  {
        
    "title":"reka",
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

reka_object_geo = {
    "id": "",
    "latitude": "",
    "longitude": ""
}

def parsePage(reka_object_link,reka_id):
    reka_object_data['id'] = reka_id
    reka_object_data['resource']['link'] = reka_object_link
    site_id = str(uuid4())
    site_id = site_id.replace('-', "")
    reka_object_data['id'] = f'{reka_id}_{site_id}'
    # имя файла 
    if reka_object_link[-1] != "/": reka_object_link+='/'
    filename = reka_object_link.split('/')[-2]
    
    url = reka_object_link
    page = requests.get(url)
    
    if page.status_code==404: return
    
    soup = BeautifulSoup(page.content, "html.parser")

    # НАЗВАНИЕ
    title_tag = soup.find("h1", attrs={"class": "name"})
    reka_object_data['realEstate']['title'] = (str(title_tag.contents[0]))
    
    # ОПИСАНИЕ
    description_div = soup.find_all("div", attrs={"class": "lot"})
    for span in description_div:
        # print(span)
        
        try:
            print(span.contents)
            if len(span.contents[0])>10:
                print(span)
        except: pass
    
    span_list = soup.find_all('span')
    for i  in range (len(span_list)):
        # ПЛОЩАДЬ
        try:
            if  span_list[i]['class']==['name'] and span_list[i].contents==['Площадь']:  
                area = str(span_list[i+1].contents[0])
                reka_object_data['realEstate']['area'] = area
            
        except Exception as e: pass

        # ЦЕНА
        try:
            if  span_list[i]['class']==['name'] and span_list[i].contents==['ГАП']:  
                price = str(span_list[i+1].contents[0])
                reka_object_data['realEstate']['totalPrice'] = price

        except Exception as e: pass
        
        
        # КАРТИНКИ
        pictures = soup.find_all('picture')
        for picture in pictures:
            try:
                if 'веб' not in picture.find('img')['src']:
                    reka_object_data['photo_link'].append('https://www.reka.fm'+picture.find('img')['src'])
                    
            except: pass
            
        
    # ГЕОЛОКАЦИЯ - НЕ ДЕЙСТВИТЕЛЬНА - ВЕДЕТ В ОФИС КОМПАНИИ 
    # a_geo_list = soup.find_all('a', attrs={"class": "ui-linkFade"} ) 
    # for a_geo in a_geo_list:
    #     try:
    #         if 'yandex.ru/maps' in a_geo['href']:
    #             start = a_geo['href'].find('whatshere[point]=') # 17 символов
    #             end = a_geo['href'].find('&')
    #             coordinates  = a_geo['href'][start+17:end]
    #             reka_object_data['id'] = f'{reka_id}_{site_id}'
    #             reka_object_data['latitude'] = coordinates.split(',')[0]
    #             reka_object_data['longitude'] = coordinates.split(',')[1]
    #     except: pass
    
parsePage('https://www.reka.fm/catalog/proizvodstvennyy-kompleks-kmz/', '123')
import requests
import json
from bs4 import BeautifulSoup
import os
from uuid import uuid4


rentavik_object_data = {
    "id":"",
    "resource":  {
        
    "title":"rentavik",
    "link":"",
    },
    "realEstate": {
        "title":"",
        "description":"",
        "pricePerSquareMeterMonth":"",
        "pricePerSquareMeterYear":""
},
"address":{
        "country":"",
        "city":"",
        "region":"",
        "street": ""
},
"photo_link": [
    
],
"details": {
    
    }
}

rentavik_object_geo = {
    "id":"",
    "latitude": "",
    "longitude": ""
}

if not os.path.exists('./rentavik_json'):
    os.makedir("./rentavik_json")
    
rentavik_id = str(uuid4())
rentavik_id = rentavik_id.replace("-","")

with open ('./log/rentavik.log') as logfile:
    for rentavik_object_link in logfile:
        rentavik_object_link = rentavik_object_link.replace('\n','')
        rentavik_object_link = 'https://www.rentavik.ru/'+rentavik_object_link
        
        filename = rentavik_object_link.split("/")[-1] if len(rentavik_object_link.split("/")[-1])!=0 else rentavik_object_link.split("/")[-2]

        print(filename)
filename = ''
page = requests.get('https://www.rentavik.ru//arenda/novostroevskaya-8/')
if page.status_code==404:
    with open(f'./rentavik_json/NOTFOUND_{filename}.json', 'w', encoding='utf-8') as fp:
        fp.write('404 NOT FOUND')    
        # continue
soup = BeautifulSoup(page.content, "html.parser")

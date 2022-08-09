import requests
import json
from bs4 import BeautifulSoup
import re

portal_object_data = {
    "id":"",
    "resource":  {
        
    "title":"kf.expert",
    "link":"",
    },
"realEstate": {
    "title":"",
    "description":"",
    "pricePerSquareMeter":""
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
            
portal_object_link = 'https://portal-da.ru/objects/250652-ofisnoe-pomeschenie-nezhiloe-pomeschenie-ploschadyu-112-6-kv-m'
url = portal_object_link
page = requests.get(url)
# print(page.status_code==302 or page.status_code==307)

soup = BeautifulSoup(page.content,"html.parser")
token = soup.find('meta',attrs={"name": "csrf-token"})
script_string = token.script.string
script_string = script_string[12:-6]
script_string = "{"+script_string+"}"

# script_string = script_string.replace(';', ',')
# script_string = script_string.replace('\\','')
# script_string = script_string.replace('\n','')
script_string = script_string.split("general.price =")[1]
script_String = script_string.replace('\n', '').replace('=', ':').replace('"true"', 'true').replace('"false"', 'false')



filename = portal_object_link.split('/')[-1]

with open(f'./portal_json/{filename}.txt', 'w',encoding='utf-8') as fp:
    fp.write(script_string)

script_json = json.loads(script_string)

with open(f'./portal_json/{filename}.json', 'w',encoding='utf-8') as fp:
    fp.write(script_json)
# print(script_json) 



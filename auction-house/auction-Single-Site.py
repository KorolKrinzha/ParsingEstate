import requests
import json
from bs4 import BeautifulSoup
import os
from uuid import uuid4

auction_object_data = {
    "id":"",
    "resource":  {
        
    "title":"auction-house",
    "link":"",
    },
"realEstate": {
    "title":"",
    "description":"",
    "totalPrice":""
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

if not os.path.exists('./auction_json'):
    os.makedirs('./auction_json')
    
auction_id = str(uuid4())
auction_id = auction_id.replace("-","")



with open('./log/auction.log') as logfile:
    for auction_object_link in logfile:
        print(logfile)
        
auction_object_link = "https://auction-house.ru/catalog/l-30000111803/"
auction_object_data['realEstate']['link'] = auction_object_link
site_id = str(uuid4())
site_id = site_id.replace('-', "")
auction_object_data['id'] = f'{auction_id}_{site_id}'

filename = auction_object_link.split("/")[-1] if len(auction_object_link.split("/")[-1])!=0 else auction_object_link.split("/")[-2]
url = auction_object_link
page = requests.get(url)


if page.status_code==404:
    with open(f'./auction_json/NOTFOUND_{filename}.json', 'w', encoding='utf-8') as fp:
        fp.write('404 NOT FOUND')    

soup = BeautifulSoup(page.content, "html.parser")


# НАЗВАНИЕ
title_tag = soup.find("meta", attrs={"property": "og:title"})
auction_object_data['realEstate']['title']= title_tag['content']

# ОПИСАНИЕ
description_complete = ''
description_div = soup.find_all("div", attrs={'class': 'page-content'})
for description in description_div:
    if description.find('p'):
        for paragraph in description.find_all('p'):
            if paragraph.string!=None:description_complete+= paragraph.string+" "
auction_object_data['realEstate']['description'] = description_complete


# АДРЕС
auction_object_data['address']['country'] = "Россия"

address_tag = soup.find("a",attrs={'href': '#mapDialog'})
try:
    address_complete = address_tag.contents[1]
    addresses = address_complete.split(",")
    
    for address_piece in addresses:
        if address_piece.startswith(" г.") or address_piece.startswith("г."):
            auction_object_data['address']['city'] = address_piece
        if address_piece.startswith(" ул.") or address_piece.startswith("ул."):
            auction_object_data['address']['street'] = address_piece
        if address_piece.endswith('область'):
            auction_object_data['address']['region'] = address_piece

            
            
            
    
except Exception as e:
    print(e)
    address_complete = str(address_tag.string) + str(address_tag.contents[0])
    auction_object_data['address']['street'] = address_complete

# ПИКЧИ

for image_item in soup.find_all('div', attrs={'class':'item'}):
    image_src = image_item.contents[1].img['src']
    image_host = ''.join(auction_object_link.split("/")[0:3])
    image_link = image_host+image_src
    auction_object_data['photo_link'].append(image_link)


# ЦЕНА
dynamic_tag = soup.find('div', attrs={'class':'element-buyout'})
price_string = dynamic_tag.dd.string
price_string = price_string.split('.')[0]
price_string = price_string.replace(" ",'')
price_int = int(price_string)

# общая цена
auction_object_data['realEstate']['totalPrice'] = price_int

with open(f'./auction_json/{filename}.json', 'w', encoding='utf-8') as fp:
    json_data = json.dumps(auction_object_data,ensure_ascii=False, indent=4)
    fp.write(json_data)


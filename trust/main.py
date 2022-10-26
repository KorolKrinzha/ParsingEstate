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
trust_id = '8fd68360cfb843ab9242ece68748f4b8'


# создаем папку куда суем результаты
if not os.path.exists('./result'):
    os.makedirs('./result')

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
    "region":"",
    "city":"",
    "street":""
},
"photo_link": [
    
]    
}



url = 'https://www.trust.ru/development/property/'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
link_list = soup.find_all('article', attrs={'class':'card__inner cards-list__card-inner'})
for link in pbar(link_list):
    
    
    # ССЫЛКА
    trust_object_link = 'https://www.trust.ru'+ str(link.find('a')['href'])
    trust_object_data['resource']['link'] = trust_object_link
    # ЦЕНА
    try:
        price = str(link.find('p', attrs={'class':'text text--big text--bold card__price'}).contents[0])
        price = " ".join(price.split())
        trust_object_data['realEstate']['totalPrice'] = price
    except Exception as e: pass
    
    # НАЗВАНИЕ
    try:
        div_title = link.find('div', attrs={'class':'title title--small card__title cards-list__item-title'})
        title = str(div_title.contents[0])
        title = " ".join(title.split())
        trust_object_data['realEstate']['title'] = title
    except: pass
    
    # АДРЕС
    try:
        span_address = link.find('span', attrs={'class':'text text--medium card__text'})
        address = str(span_address.contents[0])
        address = " ".join(address.split())
        trust_object_data['address']['country'] = 'Россия'
 
        # пример вывода Ханты-Мансийский автономный округ , г. XXXXX, ул. XXXXX, д. XX
        # ИЛИ Москва , ул. XXXXX, вл XXXX
        
        # Делаем развилку. Массив разделен через запятые  
        # Если в массиве три элемента, записываем их как город-улица
        # Если в массиве четыре элемента, записываем их как область-город-улица
        address_list = address.split(',')
        if len(address_list)==4:
            trust_object_data['address']['region'] = address_list[0]
            trust_object_data['address']['city'] = address_list[1]
            trust_object_data['address']['street'] = ''.join(address_list[2:])
        else:
            trust_object_data['address']['city'] = address_list[0]
            trust_object_data['address']['street'] = ''.join(address_list[1:])
        
    except: pass
    
    
    
    parsePage(trust_object_data, trust_id)    
        

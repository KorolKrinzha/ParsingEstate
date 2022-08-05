import requests
import json
from bs4 import BeautifulSoup
from base64 import urlsafe_b64encode
import os
from uuid import uuid4


if not os.path.exists('./kf_json'):
    os.makedirs('./kf_json')
    
kf_id = str(uuid4())
kf_id = kf_id.replace('-',"")
print(kf_id)

with open('./log/pm2.log') as logfile:
    for kf_object_link in logfile:
        kf_object_link = kf_object_link.replace('\n', '')
        filename = kf_object_link.split('/')[-1]

    
# kf_object_link = '/gorod/zhilye-kompleksy/woods-id47504'
        # try:
        try:
            url = f"https://kf.expert{kf_object_link}"
            page = requests.get(url)  # This page outputs the HTML code of the page.
            if page.status_code==404:
                with open(f'./kf_json/NOTFOUND_{filename}.json', 'w', encoding='utf-8') as fp:
                    fp.write('404 NOT FOUND')    
                    continue

                

            soup = BeautifulSoup(page.content, "html.parser")

            kf_object_data = {
                "id":"",
                "resource":  {
                    
                "title":"kf.expert",
                "link":kf_object_link,
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
            
            site_id = str(uuid4())
            site_id = site_id.replace('-', "")
            print(site_id)
            kf_object_data["id"] = f'{kf_id}_{site_id}'

            # НАЗВАНИЕ
            title_tag = soup.find('h1')
            kf_object_data['realEstate']['title'] = title_tag.string

            # АДРЕС
            address_complete = []
            address_header = soup.find('div',class_= "detail-jk-header")
            for address in soup.find_all('span', class_='detail-jk-header__address'):
                address_complete.append(address.string)
                
            kf_object_data['address']['country'] = "Россия"
            kf_object_data['address']['city'] = "Москва"
            print(address_complete)
            try:
                kf_object_data['address']['region'] = address_complete[0]+" "+address_complete[1]
                kf_object_data['address']['street'] = address_complete[2]+ " "+ address_complete[3]
            except:
                kf_object_data['address']['street'] = address_complete[0]+" "+address_complete[1]

                

            # # ПИКЧИ
            pictures = set()
            for picture_container in soup.find_all('picture', class_='swiper-zoom-container'):
                kf_object_data['photo_link'].append(picture_container.find('img')['data-src'])
                

            # # ОПИСАНИЕ
            description_complete = ''
            try:
                description = soup.find('div', class_='description section-with-id')
                for line in description.find_all('p'):
                    strong_tag = soup.strong
                    strong_tag.decompose()

                    if line.string!=None:
                        description_complete+= line.string.strip()+" "
            except:
                description = soup.find('div', class_='characteristic section-with-id')
                for line in description.find_all('p'):
                    strong_tag = soup.strong
                    strong_tag.decompose()

                    if line.string!=None:
                        description_complete+= line.string.strip()+" "

                

            kf_object_data['realEstate']['description'] = description_complete


            # # ДЕТАЛИ
            details = soup.find('div', class_='characteristic section-with-id')
            for detail in details.find_all('div', class_='characteristic__item-title'):
                item_title = detail.string
                kf_object_data['details'][item_title] = ''

            try:
                details_complete = []
                details = soup.find('div', class_='characteristic section-with-id')
                for detail in details.find_all('div',class_='characteristic__item-text'):
                    item_text = detail.find('span')
                    if item_text.string!=None:
                        details_complete.append(item_text.string)

                kf_object_data['details']['Продажа'] = details_complete[0]
                kf_object_data['details']['Готово'] = details_complete[1]
                kf_object_data['details']['Площадь, м²'] = details_complete[2]
                kf_object_data['details']['Количество квартир'] = details_complete[3]
                kf_object_data['details']['Высота потолков'] = details_complete[4]
                kf_object_data['details']['Адрес'] = details_complete[5]
                kf_object_data['details']['Метро'] = details_complete[6]


            except Exception as e:
                print(e)


                    

            # ЦЕНА ЗА КВАДРАТНЫЙ МЕТР
            try:
                price_info = soup.find('div', class_='detail-jk-preview__price-meter active')
                kf_object_data['realEstate']['pricePerSquareMeter'] =  price_info.string.strip()
            except:
                kf_object_data['realEstate']['pricePerSquareMeter'] =  'ПО ЗАПРОСУ'



            with open(f'./kf_json/{filename}.json', 'w', encoding='utf-8') as fp:
                json_data = json.dumps(kf_object_data, 
                                    ensure_ascii=False, indent=4)
                fp.write(json_data)  
        
        
        except Exception as error:
            print(error)
            with open(f'./kf_json/ERROR_{filename}.json', 'w', encoding='utf-8') as fp:
                fp.write(str(error))    



            
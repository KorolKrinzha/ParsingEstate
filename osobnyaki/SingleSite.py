import requests
import json
from bs4 import BeautifulSoup, Comment
import os
from uuid import uuid4


def cyrillic_match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())

def parsePage(osob_object_link, filename):
    

    
    # открываем уже созданный файл, в который мы уже добавили:
    # - region 
    # - link
    # - title
    # - id

     
     
        
    with open(f'./result/{filename}.json', 'r+', encoding='utf-8') as f:
        osob_object_data = json.loads(f.read())
        url = osob_object_link
        page = requests.get(url)
        
        if page.status_code==404: return
        
        soup = BeautifulSoup(page.content, "html.parser")

        # ЦЕНА
        price = soup.find('meta', attrs={'itemprop':'price'})
        try:
            osob_object_data['realEstate']['totalPrice'] = str(price['content']) 
        except: pass
        
        # ПЛОЩАДЬ
        i_square = soup.find('i', attrs={'class':'icon_square'})
        try:
            # после иконки сразу же идет площадь
            area= str(i_square.next_sibling)
            osob_object_data['realEstate']['area'] = area
        except: pass 

        # МЕТРО
        div_metro = soup.find('div', attrs={'class':'metro'})
        try:
            for content in div_metro.contents:
                # только метро содержит кириллицу. Остальное это тэги и svg 
                if cyrillic_match(str(content)):
                    metro = str(content)
                    metro = metro.replace('\n', '').replace('\t', '')
                    metro = " ".join(metro.split())
                    osob_object_data['address']['metro'] = metro
                
        except: pass
        
                    
        
        #ОПИСАНИЕ 
        div_description = soup.find('div', attrs={'itemprop':'description'})
        osob_object_data['realEstate']['description'] =  str(div_description.contents[0])
        
        # КАРТИНКИ
        a_pictures_list = soup.find_all('a', attrs={'class':'fancybox_image_carousel'})
        for picture_tag in a_pictures_list:
            try:
                photo_link = 'https://osobnyaki.com'+picture_tag['href']
                osob_object_data['photo_link'].append(photo_link)
            except: pass
        
        
        json_data_update = json.dumps(
            osob_object_data, ensure_ascii=False, indent=4)
        f.seek(0)
        f.write(json_data_update)


    
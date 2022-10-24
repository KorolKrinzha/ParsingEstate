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
rentavik_id = 'c110ffa55d6a43eeb1a12da21aac44c9'


# создаем папку куда суем результаты
if not os.path.exists('./result'):
    os.makedirs('./result')

# структура файла с основной информацией
rentavik_object_data = {
    "id": "",
    "resource": {

        "title": "rentavik",
        "link": "",
    },
    "realEstate": {
        "title": "",
        "description": "",
        "pricePerMonth": "",
        "pricePerSquareMeterYear": ""
    },
    "address": {
        "country": "",
        "city": "",
        "region": "",
        "street": ""
    },
    "photo_link": [

    ],
    "details": {

    }
}

# структура файла с гео информацией
rentavik_object_geo = {
    "id": "",
    "latitude": "",
    "longitude": ""
}




for pageNumber in pbar(range(1, 191 + 1)):

    url = f"https://www.rentavik.ru/catalog/i/?PAGEN_1={pageNumber}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    for tag in soup.find_all('script'):
        objectINMapSuspect = str(tag.string).strip()
        try:
            if objectINMapSuspect[0:11] == 'objectInMap':
                try:
                    # получение jsonА
                    building_string = objectINMapSuspect[20:].strip()
                    building_string = building_string.replace("'", '"')
                    building_string = building_string.replace('\n', ' ')
                    json_building = json.loads(building_string)

                    site_id = str(uuid4())
                    site_id = site_id.replace('-', "")
                    rentavik_object_data['id'] = f'{rentavik_id}_{site_id}'
                    rentavik_object_geo['id'] = f'{rentavik_id}_{site_id}'
                    rentavik_object_link = 'https://www.rentavik.ru' + \
                        json_building['link']
                    rentavik_object_data['resource']['link'] = rentavik_object_link
                    try:
                        latitude = json_building['geo'].split(',')[0]
                        longtitude = json_building['geo'].split(',')[1]
                        rentavik_object_geo['latitude'] = latitude
                        rentavik_object_geo['longitude'] = longtitude
                    except BaseException:
                        pass
                    rentavik_object_data['realEstate']['title'] = json_building['name']

                    rentavik_object_data['address']['country'] = 'Россия'
                    for address_piece in json_building['address'].split(','):
                        if address_piece.startswith(" г.") or address_piece.startswith("г.") \
                                or address_piece.startswith("г") or address_piece.startswith(" г"):
                            rentavik_object_data['address']['city'] = address_piece

                        if address_piece.startswith(" ул.") or address_piece.startswith("ул.")\
                                or address_piece.startswith("ул") or address_piece.startswith(" ул"):
                            rentavik_object_data['address']['street'] = address_piece

                        if address_piece.endswith('область'):
                            rentavik_object_data['address']['region'] = address_piece

                    filename = rentavik_object_link.split(
                        "/")[-1] if len(rentavik_object_link.split("/")[-1]) != 0 else rentavik_object_link.split("/")[-2]

                    # записываем геолокацию и больше не трогаем
                    with open(f'./result/GEO_{filename}.json', 'w', encoding='utf-8') as fp:
                        # записываем в json_data  json с геолокацией 
                        json_data = json.dumps(
                            rentavik_object_geo, ensure_ascii=False, indent=4)
                        fp.write(json_data)

                    # записываем в файл основной - прогодится во время выполнения функции
                    with open(f'./result/{filename}.json', 'w', encoding='utf-8') as fp:
                        # записываем в json_data значения основного json
                        json_data = json.dumps(
                            rentavik_object_data, ensure_ascii=False, indent=4)

                        fp.write(json_data)
                        # передаем имя файла. С помощью него отследим файл
                        # после парсинга отдельной страницы запишем доп инфу о нем
                        parsePage(filename)

                except Exception as e:
                    pass

        except BaseException:
            pass

import requests
import json
from bs4 import BeautifulSoup, Comment
import os
from uuid import uuid4


def parsePage(filename):
    with open(f'./result/{filename}', 'r+', encoding='utf-8') as json_data:
        rentavik_object_data = json.loads(json_data.read())

        rentavik_object_link = rentavik_object_data['resource']['link']
        print(rentavik_object_link)
        page = requests.get(rentavik_object_link)

        soup = BeautifulSoup(page.content, "html.parser")
        # ОПИСАНИЕ

        paragraph_blacklist = [
            'Пользовательское соглашение',
            'Политика конфидициальности',
            'Согласие на получение рекламных рассылок']
        for suspect_p in soup.find_all('p'):
            if suspect_p.get('href') is None and suspect_p.get('class') is None and suspect_p.string is not None\
                    and not (suspect_p.string in paragraph_blacklist):
                rentavik_object_data['realEstate']['description'] = suspect_p.string
                break

        # ДЕТАЛИ
        details_suspects = soup.find_all('div', attrs={"class": "cell"})
        for i in range(len(details_suspects)):
            detail_key = details_suspects[i].find(
                'div', attrs={'class': 'page-table__label'})
            if detail_key is not None:

                detail_value = details_suspects[i + 1].find(
                    'div', attrs={'class': 'page-table__value'})
                if detail_value is not None:
                    detail_key = detail_key.string
                    detail_key = detail_key.replace(
                        '\r', '').replace('\n', '').strip()

                    detail_value = detail_value.string
                    detail_value = detail_value.replace(
                        '\r', '').replace('\n', '').strip()
                    rentavik_object_data['details'][detail_key] = detail_value

        # ПИКЧИ
        slides_tag = [
            slides.find(
                'div', attrs={
                    'class': 'clients-slide__image'}) for slides in soup.find_all(
                'div', attrs={
                    "class": "clients-slide"})]
        for slide_tag in slides_tag:
            try:
                img_source = slide_tag.find('img')['src']
                img_link = 'https://www.rentavik.ru/' + img_source
                rentavik_object_data['photo_link'].append(img_link)
            except BaseException:
                continue

        # ЦЕНА
        for price_info in soup.find_all(
            'div', attrs={
                'class': 'filterresults-offer-prices__value'}):
            price_text = " ".join(
                price_info.find_all(
                    text=lambda t: not isinstance(
                        t, Comment)))
            price_text = price_text.replace('\n', '')
            if 'руб./м 2  в год' in price_text:
                price_text = price_text.replace(
                    'руб./м 2  в год',
                    '').replace(
                    ' ',
                    '')
                rentavik_object_data['realEstate']['pricePerSquareMeterYear'] = int(
                    price_text)
            if 'руб./мес' in price_text:
                price_text = price_text.replace(
                    'руб./мес', '').replace(' ', '')
                rentavik_object_data['realEstate']['pricePerMonth'] = int(
                    price_text)

        json_data_update = json.dumps(
            rentavik_object_data, ensure_ascii=False, indent=4)
        json_data.seek(0)
        json_data.write(json_data_update)

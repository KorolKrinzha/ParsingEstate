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
reka_id = 'de38fb63afe34e58a960a4fb153403c5'

# создаем папку куда суем результаты
if not os.path.exists('./result'):
    os.makedirs('./result')


url = 'https://www.reka.fm/catalog/?tab=tab-buying'
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
a_link_list = soup.find_all('a', attrs={'class': 'link'})
for a_llink in a_link_list:
    try:
        parsePage('https://reka.fm'+str(a_llink['href']),reka_id)
    except: pass
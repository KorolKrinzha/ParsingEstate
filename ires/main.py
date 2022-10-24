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
ires_id = '6c139cbadf6e41ce98b51f95bad6bece'


# создаем папку куда суем результаты
if not os.path.exists('./result'):
    os.makedirs('./result')



with open("URLS.html", encoding="utf-8") as fp:
    data = fp.read() 
    soup = BeautifulSoup(data, "html.parser")
    div_list = soup.find_all("div", attrs={'class': 'col-xs-4'})
    for div in pbar (div_list):
        ires_object_link = div.find('a')['href'] 
        parsePage(ires_object_link, ires_id)


        
 
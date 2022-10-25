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
dom_id = '8db22dfaf36c44b28f66ff5a0eb187f3'

# создаем папку куда суем результаты
if not os.path.exists('./result'):
    os.makedirs('./result')

# этот способ не работает - только архивы были найдены в этом sitemap
'''
url = 'https://xn--d1aqf.xn--p1ai/upload/sitemaps/sitemap_iblock_7.xml'
page = requests.get(url)

soup = BeautifulSoup(page.content,'lxml')
a_link_list = soup.find_all('url')
for a_llink in pbar (a_link_list):
    try:
        # a_llink.contents[0] - <loc>URL</loc>
        # a_llink.contents[0].contents[0] - URL
        dom_object_link = str(a_llink.contents[0].contents[0])
        parsePage(dom_object_link, dom_id)
    except Exception as e: print(e) 
    '''
    
html_count =  6   
for html_index in pbar (range(1,html_count)):
    with open(f'./URLS/URLS-{html_index}.html', encoding='utf-8') as fp:
        data = fp.read()
        soup = BeautifulSoup(data, "html.parser")
        a_link_list = soup.find_all('a', attrs={"class":"link-full-block"})
        for a_link in a_link_list:
        
            dom_object_link = 'https://xn--e1adnd0h.xn--d1aqf.xn--p1ai'+str(a_link['href'])
            parsePage(dom_object_link, dom_id)

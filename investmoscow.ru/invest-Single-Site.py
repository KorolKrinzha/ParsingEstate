import requests
import json
from bs4 import BeautifulSoup
import os
from uuid import uuid4



if not os.path.exists('./invest_json'):
    os.makedirs('./invest_json')
    
invest_id = str(uuid4())
invest_id = invest_id.replace('-',"")

with open('./log/pm2.log') as logfile:
    for invest_object_link in logfile:
        invest_object_link = invest_object_link.replace('\n', '')
        filename = invest_object_link.split('/')[-1]

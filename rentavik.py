import requests
import json
from bs4 import BeautifulSoup


url = f"https://rentavik.ru/"
page = requests.get(url)  # This page outputs the HTML code of the page.


soup = BeautifulSoup(page.content, "html.parser")
# soup = BeautifulSoup(you, "html.parser")
# print(soup)

print(soup)
for tag in soup.find_all('script'):
    
    objectINMapSuspect = str(tag.string).strip()
    try:
        if objectINMapSuspect[0:11]=='objectInMap':
            try: 
                building_string = objectINMapSuspect[20:].strip()
                building_string = building_string.replace("'", '"')
                building_string = building_string.replace('\n', ' ')
                json_buildnig = json.loads(building_string)
                # print(json_buildnig)
            except Exception as e: print(e)
        else:
            # print(objectINMapSuspect)
            pass

            
    except:
        pass
        
    

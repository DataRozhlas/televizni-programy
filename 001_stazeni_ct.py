import os
from datetime import date, datetime, timedelta
import requests

kam = "downloads/ct"
os.makedirs(kam, exist_ok=True)

stazene = os.listdir(kam)
stazene = [file for file in os.listdir(kam) if os.path.getsize(os.path.join(kam, file)) > 50]
stazene

datum = date.today()

kanaly = ["ct1","ct2","ct24","ct4","ct5","ct6","ct7"]

start = date(2005, 1, 1)
konec = date.today()
data = []
aktualni = start
while aktualni <= konec:
    print(aktualni)
    for kanal in kanaly:
        try:    
            soubor = f"""{aktualni.strftime("%Y-%m-%d")}-{kanal}.json"""
            if soubor not in stazene:
                url = f"""https://www.ceskatelevize.cz/services-old/programme/xml/schedule.php?user=kasparek&date={aktualni.strftime("%d.%m.%Y")}&channel={kanal}&json=1"""
                print(url)
                response = requests.get(url)
                if response.status_code == 200:
                    with open(os.path.join(kam, soubor), "w+", encoding='utf-8') as file:
                        file.write(response.text)
            else:
                pass
        except Exception as e:
            print(e)
    aktualni += timedelta(days=1)

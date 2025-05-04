import os
import time
import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

vsechno = True

def date_to_timestamp(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return int(date_obj.timestamp())

def stahni_fdb(datum):

    global stazene_soubory

    unixdatum = date_to_timestamp(datum)

    slozka = "downloads/fdb/"
    os.makedirs(slozka, exist_ok=True)

    urls = [
        f'https://www.fdb.cz/tv/1-ct1-ct2-nova-prima-nova-action-prima-hd-ct-3.html?datum={unixdatum}&cas_od=0',
        f'https://www.fdb.cz/tv/4-nova-cinema-tv-barrandov-prima-cool-prima-love-cnn-prima-news-film-europe-channel-nova-fun-nova-lady-prima-show-prima-star.html?datum={unixdatum}&cas_od=0',
        f'https://www.fdb.cz/tv/3-cinemax-cinemax2-cs-film-film.html?datum={unixdatum}&cas_od=0',
        f'https://www.fdb.cz/tv/7-markiza-joj-plus-voyo-nova-2-joj-hd-plus-hd-joj.html?datum={unixdatum}&cas_od=0'
    ]

    for url in urls:

        soubor = f'fdb_{datum}_{url.split("?")[0].split("/")[-1]}'

        if soubor not in stazene_soubory:

            try:

                r = requests.get(url)
                with open(os.path.join(slozka, soubor), "w+", encoding="utf-8") as program:
                    program.write(r.text)

                print(f"Stažen program {soubor}")

            except Exception as e:
                print(e)
                time.sleep(300)
                r = requests.get(url)
                with open(os.path.join(slozka, soubor), "w+", encoding="utf-8") as program:
                    program.write(r.text)

                print(f"Snad stažen program {soubor}, nutno zkontrolovat.")

    
def vygeneruj_data():
    
    start = date.fromisoformat("2007-01-01")
    end = date.fromisoformat("2025-04-16")
    seznam = [start.strftime('%Y-%m-%d')]

    while start <= end:
        start += relativedelta(days=1)
        seznam.append(start.strftime('%Y-%m-%d'))

    return seznam

if vsechno == True:
    
    data = vygeneruj_data()
    stazene_soubory = set([x for x in os.listdir("downloads/fdb/") if ".html" in x])
    print(f"Stažených souborů: {len(stazene_soubory)}")

    try:
        stazene = [x.split("_")[1] for x in os.listdir("downloads/fdb/")]
        ## háček k dořešení: je-li stažený jen jeden program za daný den, celý den se považuje za stažený
    except:
        stazene = []

    # data = [d for d in data if d not in set(stazene)]

    for d in data:
        stahni_fdb(d)

else:

    stazene_soubory = []
    stahni_fdb(date.today().strftime('%Y-%m-%d'))
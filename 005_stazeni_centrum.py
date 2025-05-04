import os
from dateutil.relativedelta import relativedelta
from datetime import date
import nest_asyncio; nest_asyncio.apply()  # This is needed to use sync API in repl
from playwright.sync_api import sync_playwright

vsechno = False

def stahni_centrum(datum):

    slozka = f"downloads/centrum/{datum.replace("/","-")}"
    os.makedirs(slozka, exist_ok=True)
    url = f"https://tvprogram.centrum.cz/den/{datum}"

    try:

        with sync_playwright() as pw:
            browser = pw.firefox.launch(headless=True)
            context = browser.new_context(viewport={"width": 1920, "height": 1080, "timezone_id": "Europe/Berlin"})
            page = context.new_page()

            page.goto(url)
            page.wait_for_timeout(5000)

            with open(os.path.join(slozka, f'centrum_{datum.replace("/","-")}.html'), "w+", encoding="utf-8") as program:
                program.write(page.content())

            print(f'Program za {datum} stažen.')

    except Exception as e:
        print(e)

    finally:
        page.close()
        context.close()
        browser.close()
    
def vygeneruj_data():
    
    start = date.fromisoformat("2022-02-01")
    end = date.fromisoformat("2025-01-19")
    seznam = [start.strftime('%Y/%m/%d')]

    while start <= end:
        start += relativedelta(days=1)
        seznam.append(start.strftime('%Y/%m/%d'))

    return seznam

if vsechno == True:
    
    data = vygeneruj_data()
    for d in data:
        stahni_centrum(d)

else:
    stahni_centrum(date.today().strftime('%Y/%m/%d'))
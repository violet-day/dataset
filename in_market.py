
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import schedule
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import  *

from selenium import webdriver

def init():
    if is_linux():
        service = Service(chrome_binary_location_linux)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--enable-javascript')
        options.add_argument('--enable-cookies')

        for header_key, header_value in headers.items():
            options.add_argument(f'{header_key}={header_value}')
        options.add_argument(f'--user-agent={user_agent}')

        # 创建 Chrome 浏览器驱动实例，并传入 Service 对象
        driver = webdriver.Chrome(service=service, options=options)

        return driver
    else:
        service = Service(chrome_binary_location_mac)

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--enable-javascript')
        # options.add_argument('--enable-cookies')
        options.add_experimental_option(
            "prefs", {
                # block image loading
                "profile.managed_default_content_settings.images": 2,
            }
        )
        for header_key, header_value in headers.items():
            options.add_argument(f'{header_key}={header_value}')
        options.add_argument(f'--user-agent={user_agent}')

        # 创建 Chrome 浏览器驱动实例，并传入 Service 对象
        driver = webdriver.Chrome(service=service, options=options)
    return driver

def top_gainer():
    try:
        start_url = 'https://stockanalysis.com/markets/gainers/'
        with init() as driver:
            driver.get(start_url)
            text = driver.page_source.encode("utf-8")
            logging.info('get text success')
            soup = BeautifulSoup(text, features='html.parser')
            tables = soup.find_all(attrs={'id': 'main-table'})
            if len(tables) == 0:
                logging.warning('No tables found')
            table = tables[0]
            trs = table.find('tbody').find_all('tr')
            tickers = []
            for tr in trs:
                tickers.append(tr.find_all('td')[1].text.strip())
            return tickers
    except Exception as e:
        return []

def job():
    now = get_eastern_now()
    day = now.strftime('%y%m%d')
    import os
    os.makedirs('data/inmarket/daily/', exist_ok=True)
    # if now.weekday() < 5 and now.replace(hour=9, minute=30) <= now <= now.replace(hour=16, minute=0):
    if True:
        logging.info('in market time')
        gainers = top_gainer()
        logging.info(f'fetch top gainer {gainers}')
        with open(f'data/inmarket/daily/{day}.csv', 'a+') as f:
            for g in gainers:
                f.writelines(now.strftime('%Y-%m-%d %H:%M') + ',' + g + '\n')

if __name__ == '__main__':
    logging.info('hi nemo')
    job()
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

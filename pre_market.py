import logging
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import schedule
import time
from common import  *



def top_gainer():
    try:
        chrome_options = Options()
        if is_linux():
            chrome_options.binary_location = chrome_binary_location_linux
        else:
            chrome_options.binary_location = chrome_binary_location_mac
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        if is_linux():
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless=new")  # for Chrome >= 109
        for header_key, header_value in headers.items():
            chrome_options.add_argument(f'{header_key}={header_value}')

        # chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        if is_linux():
            driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_linux_executable_path)
        else:
            driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_mac_executable_path)

        start_url = "https://cn.investing.com/equities/pre-market"
        driver.get(start_url)
        text = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(text, features='html.parser')
        tables = soup.find_all(attrs={'data-test': 'pre-market-top-gainers-losers-table'})
        premarket_gainers = tables[0]
        symbols = [element.text for element in premarket_gainers.find_all('span') if
                   element.text not in ['名称', '最新', '涨跌幅', '交易量']]
        logging.info(symbols)
        return symbols
    except Exception as err:
        logging.error(err)
        return []


def job():
    now = get_eastern_now()
    day = now.strftime('%y%m%d')
    if now.weekday() < 5 and now.replace(hour=4, minute=1) <= now <= now.replace(hour=9, minute=25):
        logging.info('in pre premarket time')
        gainers = top_gainer()
        with open(f'data/premarket/{day}.csv', 'a') as f:
            for g in gainers:
                f.writelines(now.strftime('%Y-%m-%d %H:%M') + ',' + g + '\n')


if __name__ == '__main__':
    logging.info('hi nemo')
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import schedule
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common import  *

from selenium import webdriver


def init():
    if is_linux():
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_binary_location_linux
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        return driver
    chrome_options = Options()
    if is_linux():
        chrome_options.binary_location = chrome_binary_location_linux
    else:
        chrome_options.binary_location = chrome_binary_location_mac
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--dns-prefetch-disable")

    if is_linux():
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--no-sandbox")  # linux only
    chrome_options.add_argument("--headless")  # for Chrome >= 109

    for header_key, header_value in headers.items():
        chrome_options.add_argument(f'{header_key}={header_value}')
    chrome_options.add_argument(f'--user-agent={user_agent}')

    # chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works
    if is_linux():
        driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=chrome_driver_linux_executable_path,
        )
    else:
        driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=chrome_driver_mac_executable_path,
        )
    return driver

def top_gainer():
    try:
        start_url = "https://cn.investing.com/equities/pre-market"
        with init() as driver:
            driver.get(start_url)

            wait = WebDriverWait(driver, timeout=45)
            wait.until(EC.title_contains('美股盘前交易'))

            text = driver.page_source.encode("utf-8")
            soup = BeautifulSoup(text, features='html.parser')
            tables = soup.find_all(attrs={'data-test': 'pre-market-gainers-table'})
            if len(tables) == 0:
                logging.info('table is empty, we may retry')
                driver.get(start_url)
                text = driver.page_source.encode("utf-8")
                soup = BeautifulSoup(text, features='html.parser')
                tables = soup.find_all(attrs={'data-test': 'pre-market-gainers-table'})
                premarket_gainers = tables[0]
                trs = premarket_gainers.find('tbody').find_all('tr')
                spans = [[s.text for s in tr.find('td').find_all('span') if len(s.text) > 0][0] for tr in trs]
                symbols = spans
                symbols = sorted(symbols)
                logging.info(symbols)
                return symbols
            else:
                premarket_gainers = tables[0]
                trs = premarket_gainers.find('tbody').find_all('tr')
                spans = [[s.text for s in tr.find('td').find_all('span') if len(s.text) > 0][0] for tr in trs]
                symbols = spans
                symbols = sorted(symbols)
                logging.info(symbols)
                return symbols
    except Exception as err:
        logging.exception(err)
        return []


def job():
    now = get_eastern_now()
    month = now.strftime('%y%m')
    import os
    os.makedirs('data/premarket/', exist_ok=True)
    if now.weekday() < 5 and now.replace(hour=4, minute=10) <= now <= now.replace(hour=9, minute=25):
        logging.info('in pre premarket time')
        gainers = top_gainer()
        with open(f'data/premarket/{month}.csv', 'a+') as f:
            for g in gainers:
                f.writelines(now.strftime('%Y-%m-%d %H:%M') + ',' + g + '\n')
    if len(gainers)>0:
        sync_to_github()

if __name__ == '__main__':
    logging.info('hi nemo')
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

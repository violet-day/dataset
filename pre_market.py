import re
import requests
from bs4 import BeautifulSoup
import logging
import schedule
import time
from datetime import datetime

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='premarket.log', level=logging.INFO, format=LOG_FORMAT)

headers = {
    'authority': 'cn.investing.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
}


def find_symbol_by_href(href):
    try:
        res = requests.get('https://cn.investing.com' + href, headers=headers).text
        re_result = re.findall('\"tickersymbol\":"\w+"', res)
        if len(re_result) == 0:
            logging.error('{} fail', href)
            return None
        tickersymbol = re_result[0]
        return tickersymbol.replace('"tickersymbol":', '').strip('"')
    except:
        return None


def top_gainer():
    try:
        response = requests.get('https://cn.investing.com/equities/pre-market', headers=headers)
        soup = BeautifulSoup(response.text)
        tables = soup.find_all(id='premarket_gainers')
        premarket_gainers = tables[0]
        results = [find_symbol_by_href(e['href']) for e in premarket_gainers.find_all('a')]
        logging.info(results)
        return [symbol for symbol in results if symbol is not None]
    except Exception as err:
        logging.error(err)
        return []


def job():
    now = datetime.now()
    if now <= now.replace(hour=16, minute=1) \
        or now >= now.replace(hour=21, minute=25):
        return
    gainers = top_gainer()
    with open('data/premarket.csv', 'a') as f:
        for g in gainers:
            f.writelines(now.strftime('%Y-%m-%d %H:%M') + ',' + g + '\n')


if __name__ == '__main__':
    logging.info('hi nemo')
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

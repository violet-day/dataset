import re
import requests
from bs4 import BeautifulSoup
import logging
import schedule
import time
from datetime import datetime, timedelta, timezone
import pytz
import sys
import os
import json

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

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

params = (
    ('country', 'usa'),
)

href_cache = dict()


def find_symbol_by_href(href):
    if href in href_cache:
        return href_cache.get(href)
    try:
        res = requests.get('https://cn.investing.com' + href, headers=headers).text
        re_result = re.findall('\"tickersymbol\":"\w+"', res)
        if len(re_result) == 0:
            return logging.error('{} fail', href)
        tickersymbol = re_result[0]
        symbol = tickersymbol.replace('"tickersymbol":', '').strip('"')
        href_cache[href] = symbol
        return symbol
    except Exception as err:
        return None


def top_gainer():
    try:
        response = requests.get('https://cn.investing.com/equities/top-stock-gainers', headers=headers, params=params)
        soup = BeautifulSoup(response.text)
        results = soup.find(id='stockPageInnerContent').find_all('table')[0].find_all('a')
        results = [(e.get_text(), find_symbol_by_href(e['href'])) for e in results]
        results = [symbol for text, symbol in results if symbol is not None]
        logging.info(results)
        return results
    except Exception as err:
        logging.error(err)
        return []


root_dir = 'data/in_mkt/'

tz_utc_8 = timezone(timedelta(hours=8))
eastern = pytz.timezone('US/Eastern')

def job():
    now = datetime.now()
    now = now.astimezone(eastern)
    today_path = os.path.join(root_dir, now.strftime('%Y-%m-%d') + '.json')
    if os.path.exists(today_path):
        with open(today_path, 'r') as f:
            data = json.load(f)
            data = {s: datetime.strptime(t, '%Y-%m-%d %H:%M:%S')  for s, t in data.items()}
    else:
        data = {}

    now = datetime.now()
    now = now.astimezone(eastern)

    if now >= now.replace(hour=9, minute=30, second=0) and now <= now.replace(hour=16, minute=0, second=0):
    #if True:
        gainers = top_gainer()
        print(gainers)
        should_add_gainers = [g for g in gainers if g not in data or (g in data and now < data.get(g))]
        for g in should_add_gainers :
            data[g] = now
        data = {s: datetime.strftime(t, '%Y-%m-%d %H:%M:%S') for s, t in data.items()}
        with open(today_path, 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    job()
    schedule.every(4).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

import re
import requests
from bs4 import BeautifulSoup
import logging
import schedule
import time
from datetime import datetime
import sys

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


def job():
    now = datetime.now()
    logging.info(now)
    if (now >= now.replace(hour=21, minute=30) and now <= now.replace(hour=23, minute=59))  or (now >= now.replace(hour=0, minute=0) and now <= now.replace(hour=4, minute=0)):

      #if now <= now.replace(hour=21, minute=30) \
      #  or now >= now.replace(hour=4, minute=00):
      #  return
      gainers = top_gainer()
      with open('data/inmarket.csv', 'a') as f:
          for g in gainers:
              f.writelines(now.strftime('%Y-%m-%d %H:%M') + ',' + g + '\n')


if __name__ == '__main__':
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

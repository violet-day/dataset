import time

import pandas as pd
import schedule
from common import upload_file


def job():
    df = pd.read_csv('data/premarket.csv', names=['time', 'symbol'])

    result = dict()

    for _, row in df.iterrows():
        date = row['time'].split(' ')[0]
        if date not in result:
            result[date] = []
        if row['symbol'] not in result[date]:
            result[date].append(row['symbol'])

    upload_file(result, '/quant/pre_mkt.json')


if __name__ == '__main__':
    job()
    schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
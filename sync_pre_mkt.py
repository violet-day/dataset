import time

import pandas as pd
import schedule
from common import upload_file


def job():
    df = pd.read_csv('data/premarket.csv', names=['time', 'symbol'])

    df['date'] = df['time'].apply(lambda t: t.split(' ')[0])

    output = df.groupby(['date', 'symbol']).min('time').reset_index()
    output = output.groupby(['time']).agg(symbols=('symbol', 'unique')).reset_index()

    result = {row['time']: list(row['symbols']) for _, row in output.iterrows()}
    upload_file(result, '/quant/pre_mkt.json')


if __name__ == '__main__':
    job()
    schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
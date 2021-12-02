import time

import pandas as pd
import pytz
import schedule
from common import upload_file
from datetime import datetime

eastern = pytz.timezone('US/Eastern')

def job():
    df = pd.read_csv('data/premarket.csv', names=['time', 'symbol'])
    df['time'] = df['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M').astimezone(eastern))
    df['date'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d'))
    df['time'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d %H:%M'))

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
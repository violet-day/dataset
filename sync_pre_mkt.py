import time
from datetime import datetime

import pandas as pd
import schedule

from common import *


def job():
    now = get_eastern_now()
    day = now.strftime('%y%m%d')
    if now.weekday() >= 5:
        return
    df = pd.read_csv(f'data/premarket-{day}.csv', names=['time', 'symbol'])
    df['time'] = df['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M'))
    df['date'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d'))
    df['time'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d %H:%M'))

    output = df.groupby(['date', 'symbol']).min('time').reset_index()
    output = output.groupby(['time']).agg(symbols=('symbol', 'unique')).reset_index()

    result = {row['time']: list(row['symbols']) for _, row in output.iterrows()}
    upload_file(result, f'/quant/pre_mkt-{day}.json')


if __name__ == '__main__':
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
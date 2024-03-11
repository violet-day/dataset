import time
from datetime import datetime

import pandas as pd
import schedule
import os.path
from common import *


def job():
    now = get_eastern_now()
    month = now.strftime('%y%m')

    if now.weekday() < 5 and now.replace(hour=4, minute=10) <= now <= now.replace(hour=9, minute=25):
        file_path = f'data/premarket/{month}.csv'
        if not os.path.exists(file_path):
            logging.error(f'{month} and has not file')
            return
        df = pd.read_csv(file_path, names=['time', 'symbol'])
        df['time'] = df['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M'))
        df['date'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d'))
        df['time'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d %H:%M'))

        output = df.groupby(['date', 'symbol']).min('time').reset_index()

        if not 'time' in output:
            logging.info(output)

        output = output.groupby(['time']).agg(symbols=('symbol', 'unique'))
        upload_file(output.to_csv(), f'/quant/premkt/{month}.csv')


if __name__ == '__main__':
    job()
    schedule.every(5).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
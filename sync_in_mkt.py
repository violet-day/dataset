from datetime import datetime, timedelta

import pandas as pd

from common import upload_file

df = pd.read_csv('data/inmarket.csv', names=['time', 'symbol'])

result = dict()

for _, row in df.iterrows():
    time = datetime.strptime(row['time'], '%Y-%m-%d %H:%M') - timedelta(hours=12)
    day = time.strftime('%Y-%m-%d')
    if day not in result:
        result[day] = dict()
    daily_log = result[day]
    symbol = row['symbol']
    if symbol not in daily_log or daily_log.get(symbol) > time:
        daily_log[symbol] = time - timedelta(minutes=5) 
    daily_log = {k: v.strftime('%Y-%m-%d %H:%M') for k, v in daily_log.items()}

logs = {d: {k: v.strftime('%Y-%m-%d %H:%M') for k, v in l.items()} for d, l in result.items()}

upload_file(logs, '/quant/in_mkt.json')

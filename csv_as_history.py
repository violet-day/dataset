import pandas as pd

df = pd.read_csv('data/premarket.csv', names=['time', 'symbol'])

result = dict()

for _, row in df.iterrows():
    date = row['time'].split(' ')[0]
    if date not in result:
        result[date] = []
    if row['symbol'] not in result[date]:
        result[date].append(row['symbol'])

lines = ['"{date}": [{symbols}],'.format(date=date, symbols=','.join(['"' + s + '"' for s in symbols])) for date, symbols in result.items()]

print('\n'.join(lines))

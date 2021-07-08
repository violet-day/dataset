import pandas as pd


def get_all_symbols():
  NASDAQ = pd.read_csv('data//NASDAQ.txt', sep='\t')
  NYSE = pd.read_csv('data/NYSE.txt', sep='\t')

  symbols = list(pd.concat([NASDAQ, NYSE])['Symbol'])
  return symbols

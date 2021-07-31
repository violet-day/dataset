import json
import os

from common import upload_file
import schedule
import time

root_dir = 'data/in_mkt/'

def reverse_symbol(symbol_log):
    result = {}
    for symbol, datetime in symbol_log.items():
        if datetime not in result:
            result[datetime] = []
        result[datetime].append(symbol)
    return result

def job():
    fs = [(p.replace('.json', ''), os.path.join(root_dir, p)) for p in os.listdir(root_dir) if p.endswith('json')]
    jsons = {day: json.load(open(file_path, 'r')) for day, file_path in fs}

    jsons = {k: reverse_symbol(v) for k, v in jsons.items()}
    upload_file(jsons, '/quant/in_mkt.json')


if __name__ == '__main__':
    job()
    schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
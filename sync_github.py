
import logging
import subprocess

from common import get_eastern_now
import schedule
import time

def job():
    now = get_eastern_now()
    if now.weekday() < 5 and now.replace(hour=4, minute=0) <= now <= now.replace(hour=16, minute=0):
    # if True:
        subprocess.run(['sh', 'sync_github.sh'])

if __name__ == '__main__':
    logging.info('hi nemo, pre sync github')
    job()
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

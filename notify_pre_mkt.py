
from email.header import Header
import smtplib
import email
import os
import pandas as pd
import schedule
import time
from common import *

password = 'd9DPORSFwQ2T'
smtp_server = 'smtp.office365.com'

sender = 'violet_day@live.com'

receivers = 'violet_day@live.com'

def notify_email(subject, text):
    message = email.message_from_string(text)

    message['From'] = sender
    message['To'] = receivers

    subject = subject
    message['Subject'] = Header(subject, 'utf-8')
    try:
        with smtplib.SMTP(smtp_server, port=587) as server:
            server.starttls()
            server.login(sender, password)
            server.ehlo()
            server.sendmail(sender, receivers, message.as_string())
            logging.info("email send success")
    except smtplib.SMTPException as err:
        logging.error(err)
        logging.exception(err)

def job():
    now = get_eastern_now()
    month = now.strftime('%y%m')
    day = now.strftime('%Y-%m-%d')

    if now.strftime('%H%M') != '0920':
        return

    if now.weekday() < 5:
        file_path = f'data/premarket/{month}.csv'
        if not os.path.exists(file_path):
            logging.error(f'{month} and has not file')
            return
        df = pd.read_csv(file_path, names=['time', 'symbol'])
        df['time'] = df['time'].apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M'))
        df['date'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d'))
        df['time'] = df['time'].apply(lambda t: t.strftime('%Y-%m-%d %H:%M'))

        # day = '2024-02-26'
        symbols = df.loc[df.date==day].symbol.unique()
        if len(symbols) > 0:
            notify_email('PreMarket Symbols', f'watched symbols is {symbols}')
        else:
            logging.warning('empty symbols')

if __name__ == '__main__':
    job()
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
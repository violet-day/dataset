import dropbox
import json

import logging
import sys

import pytz

from datetime import datetime


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

dropbox_token = 'TPVJIFt6o0AAAAAAAAAAAdVcDjALRqBkAYPyEHUGzrWf3NwRDIdHbzvbfNX0d-dI'

dbx = dropbox.Dropbox(dropbox_token)

def upload_file(data, path):
    dbx.files_upload(str.encode(json.dumps(data, indent=' ')), path, mode=dropbox.files.WriteMode.overwrite)
    logging.info(f"upload {path} success")

def get_eastern_now():
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now()
    now = now.astimezone(eastern)
    return now

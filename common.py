import dropbox
import json

dropbox_token = 'TPVJIFt6o0AAAAAAAAAAAdVcDjALRqBkAYPyEHUGzrWf3NwRDIdHbzvbfNX0d-dI'

dbx = dropbox.Dropbox(dropbox_token)

def upload_file(data, path):
    dbx.files_upload(str.encode(json.dumps(data, indent=' ')), path, mode=dropbox.files.WriteMode.overwrite)

import dropbox
import json

import logging
import sys

import pytz

from datetime import datetime


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format=LOG_FORMAT
)

headers = {
    'authority': 'cn.investing.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'udid=d8ce102bad885b84fac4a04c1f4928f3; invpro_promote_variant=0; user-browser-sessions=1; browser-session-counted=true; adBlockerNewUserDomains=1708763139; _fbp=fb.1.1708763139723.1175340010; pm_score=clear; _hjHasCachedUserAttributes=true; __eventn_id=6030f9d4-64ff-468e-b9fe-594c6c27dafa; _cc_id=687880a4ff54b803cdb9ac50f357c9ce; panoramaId_expiry=1709367940902; panoramaId=d64cdc934b4cdaa975993207431016d539384fcad0ae830360f785a9eaab1a45; panoramaIdType=panoIndiv; _pbjs_userid_consent_data=3524755945110770; _au_1d=AU1D-0100-001708763142-8J76KQ0S-TT1E; gcc=HK; gsc=; smd=d8ce102bad885b84fac4a04c1f4928f3-1708938397; __cf_bm=WVrv1YP7VjcTzjgEzG3LpgM_tBSWNkg1JOfefPrSBzY-1708938397-1.0-AfFn17VaI+BhrrLnXTy+1ahhJvvs5VhoYQUYGhQJDh7STLVXwRZFXElIp5+ysG3ERflDW8apbSfe5zwUnRXCddaUuxMC/nnHEOmOPl0l5L4m; invpc=2; lifetime_page_view_count=2; _hjSessionUser_174945=eyJpZCI6IjA1Yzg2ZTQxLWUxMjUtNTgzMS1iZTE0LTc1NTM5ODFlMDM3ZiIsImNyZWF0ZWQiOjE3MDg3NjMxNDAyMzIsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_174945=eyJpZCI6ImZlNzdjOTU1LTFhMWUtNGYyNS04ZThkLTYxNDhhMTljOGRhOSIsImMiOjE3MDg5MzgzOTgzNTEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _imntz_error=0; im_sharedid=dc554c02-f0b8-48e4-a8af-3377a80e398c; _ga_C4NDLGKVMK=GS1.1.1708938399.2.0.1708938399.60.0.0; _ga=GA1.2.1954588005.1708763141; _gid=GA1.2.1863542664.1708938399; FCNEC=%5B%5B%22AKsRol8A1yIu7gsE2OuLrO60iwuf0JWJRKEA8YAFVrhAZZ7E44y5j11jYnwwb6aAVyG0q9ruraYkvy7L4JDR92d-7ZTU-D94ISqpJX8Po4bVv9r9IPRuuxD-L6lGdZlb42XODIfNiasGLs4R_fdCMueDUQywhMsi6g%3D%3D%22%5D%5D; _au_last_seen_pixels=eyJhcG4iOjE3MDg5Mzg0MDAsInR0ZCI6MTcwODkzODQwMCwicHViIjoxNzA4OTM4NDAwLCJydWIiOjE3MDg5Mzg0MDAsInRhcGFkIjoxNzA4OTM4NDAwLCJhZHgiOjE3MDg5Mzg0MDAsImdvbyI6MTcwODkzODQwMCwic29uIjoxNzA4OTM4NDAwLCJiZWVzIjoxNzA4NzYzMTQyLCJvcGVueCI6MTcwODkzODQwMCwiY29sb3NzdXMiOjE3MDg5Mzg0MDB9; _lr_geo_location_state=; _lr_geo_location=HK; cf_clearance=T492GMrFLRls7Dr0WnOs76x0QwsWXULf5HzOF5PCcSA-1708938402-1.0-Aaze7++00fLpyqmBTfO5ksFrUQ6cFSI7bLKjWYjphZ3Ll3nWtvtsWTpyILHG7c+gvsMFOi/PyP5O+XNaHoWC+EE=; __gads=ID=d3e5ab8ecc12ce8d:T=1708763143:RT=1708938924:S=ALNI_MYnIuiqmG92kSd7TwFSMdiV4v1iOw; __gpi=UID=00000d131c3f4a4e:T=1708763143:RT=1708938924:S=ALNI_MZDcG1Vhl6L4z2hXeMUwkVENpw5bw; __eoi=ID=0632ff9e3282aeb6:T=1708763143:RT=1708938924:S=AA-AfjbHdoZSWMeZE_oYtJEaFMgD',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

dropbox_token = 'TPVJIFt6o0AAAAAAAAAAAdVcDjALRqBkAYPyEHUGzrWf3NwRDIdHbzvbfNX0d-dI'

# chrome_driver_executable_path = '/data/quant/chromedriver'
chrome_driver_executable_path = '/opt/homebrew/bin/chromedriver'
dbx = dropbox.Dropbox(dropbox_token)

def upload_file(data, path):
    dbx.files_upload(str.encode(json.dumps(data, indent=' ')), path, mode=dropbox.files.WriteMode.overwrite)
    logging.info(f"upload {path} success")

def get_eastern_now():
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now()
    now = now.astimezone(eastern)
    return now

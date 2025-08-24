import os
import requests
import logging
from config import YANDEX_TOKEN

def upload_to_yandex_disk(file_path):
    filename = os.path.basename(file_path)
    headers = {'Authorization': f'OAuth {YANDEX_TOKEN}'}
    upload_api = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    publish_api = 'https://cloud-api.yandex.net/v1/disk/resources/publish'
    meta_api = 'https://cloud-api.yandex.net/v1/disk/resources'

    try:
        params = {'path': f'disk:/Zayavki/{filename}', 'overwrite': 'true'}
        upload_resp = requests.get(upload_api, headers=headers, params=params)
        upload_url = upload_resp.json()['href']

        with open(file_path, 'rb') as f:
            requests.put(upload_url, data=f)

        requests.put(publish_api, headers=headers, params={'path': f'disk:/Zayavki/{filename}'})
        meta_resp = requests.get(meta_api, headers=headers, params={'path': f'disk:/Zayavki/{filename}'})
        return meta_resp.json().get('public_url', '')
    except Exception as e:
        logging.error(f"Ошибка загрузки на Яндекс Диск: {e}")
        return ''

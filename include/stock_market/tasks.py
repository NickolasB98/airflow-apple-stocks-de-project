from include.helpers.minio import get_minio_client
from airflow.hooks.base import BaseHook
from io import BytesIO
import requests
import json

def _get_stock_prices(url, symbol):
    url = f"{url}{symbol}?metrics=high?&interval=1d&range=1y"
    api = BaseHook.get_connection('stock_api')
    response = requests.get(url, headers=api.extra_dejson['headers'])
    return json.dumps(response.json()['chart']['result'][0])

def _store_prices(prices):
    prices = json.loads(prices)
    client = get_minio_client()
    bucket_name = 'stock-market'
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    symbol = prices['meta']['symbol']
    data = json.dumps(prices, ensure_ascii=False).encode('utf8')
    objw = client.put_object(
        bucket_name=bucket_name,
        object_name=f'{symbol}/prices.json',
        data=BytesIO(data),
        length=len(data)
        )
    return f'{objw.bucket_name}/{symbol}'
    
def _get_formatted_prices_from_minio(location):
    client = get_minio_client()
    objects = client.list_objects(f'stock-market', prefix='AAPL/formatted_prices/', recursive=True)
    csv_file = [obj for obj in objects if obj.object_name.endswith('.csv')][0]
    return f's3://{csv_file.bucket_name}/{csv_file.object_name}'
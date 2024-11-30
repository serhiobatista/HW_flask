# import clickhouse_connect
# from loguru import logger
#
#
# client = clickhouse_connect.get_client(host='127.0.0.1',
#                                        port=8123,
#                                        username='default',
#                                        database='test')



import requests, json

# url = 'http://api.openweathermap.org/data/2.5/weather?/'
# api_key='52d76186d4e1d0cd2e71c4e49e4a748a'
# city_name='Moscow'
#
# complete_url = url + "appid=" + api_key + "&q=" + city_name
# myobj = {'lat': '30', 'lon': '40', 'appid': key}
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from config.settings import settings
from databases.connections import client
import json
from datetime import datetime



# d = x.json()

# print(response['time']['updatedISO'])



complete_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
response = requests.get(complete_url).text
currency = 'EUR'
response = json.loads(response)
# print(response)
dict_time, dict_currency = response['time'], response['bpi'][currency]
dict_time.update(dict_currency)
response = json.dumps(dict_time)

res = client.query('''SELECT *
                      FROM default.bitcoin_info
                      WHERE dt = (SELECT MAX(dt) from default.bitcoin_info)
                      LIMIT 1''')
res = res.result_rows
col_names = ['dt', 'currency', 'rate']
res = [res[0][0], res[0][1], res[0][2]]
res = dict(zip(col_names, res))
res['dt'] = res['dt'].strftime('%Y-%m-%d %H:%M:%S')
res = json.dumps(response, default=str)

# print(response)
# data = res.result_rows
# for i in data:
#     print(i)
# print(data[0][0])
# dt = data[0][0]
# data[0] = dt.strftime('%Y-%m-%d %H:%M:%S')
# print(data)


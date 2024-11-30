from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from config.settings import settings
from databases.connections import client
from datetime import datetime
import requests, json

broker = RabbitBroker(url=settings.rabbit_url)
app = FastStream(broker)


@broker.subscriber(RabbitQueue(name="tasks", durable=True))
async def task(bitcoin_info: str):
    bitcoin_info = json.loads(bitcoin_info)
    create_table = client.command('CREATE TABLE IF NOT EXISTS bitcoin_info (dt DateTime, currency String, rate Float64) ENGINE MergeTree ORDER BY dt;')
    update_time = datetime.fromisoformat(bitcoin_info['updatedISO'])
    row1 = [update_time, bitcoin_info['code'],
            bitcoin_info['rate_float']]
    data = [row1]
    client.insert('bitcoin_info', data, column_names=['dt', 'currency', 'rate'])


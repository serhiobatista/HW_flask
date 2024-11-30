from config.settings import settings
import clickhouse_connect


# client = clickhouse_connect.get_client(host='127.0.0.1',
#                                        port=8123,
#                                        username='default',
#                                        database='default')

client = clickhouse_connect.get_client(**settings.clickhouse.model_dump())

from fastapi import APIRouter
from rabbit.publisher import publish_bitcoin_rate
from config.settings import settings
from databases.connections import client
import requests,json
from fastapi.responses import JSONResponse

bitcoin_router = APIRouter(tags=["bitcoin"])


@bitcoin_router.get("/send/{currency}")
async def retrieve_all_records(currency: 'str') -> dict:
    complete_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(complete_url).text
    response = json.loads(response)
    print(response)
    dict_time, dict_currency = response['time'], response['bpi'][currency]
    dict_time.update(dict_currency)
    response = json.dumps(dict_time)
    await publish_bitcoin_rate(rate=response)
    return {"message": "the bitcoin rate has been successfully added to the queue"}


@bitcoin_router.get("/data")
async def get_current_currency():
    res = client.query('''SELECT * 
                          FROM default.bitcoin_info 
                          WHERE dt = (SELECT MAX(dt) from default.bitcoin_info)''')
    res = res.result_rows
    col_names = ['dt', 'currency', 'rate']
    res = [res[0][0], res[0][1], res[0][2]]
    res = dict(zip(col_names, res))
    dt = res['dt']
    res['dt'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    # res = json.dumps(res)
    # return res
    return JSONResponse(content=res)

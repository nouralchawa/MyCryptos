from requests import Request, Session
from requests.exceptions import ConnectionError , Timeout , TooManyRedirects 
import json

url_price = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters= {
    'symbol':'BTC',
    'amount':'1',
    'convert': 'EUR'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'ff4f88a1-8c9f-4888-8548-c841771b41a3',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

convert = {
    'symbol':'BTC',
    'amount':'1',
    'convert': 'EUR',
}

try:
    response = session.get(url_price,params=convert)
    data_2 = json.loads(response.text)
    print(data_2["data"]["quote"]["EUR"]["price"])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
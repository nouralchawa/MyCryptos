from requests import Request, Session
from requests.exceptions import ConnectionError , Timeout , TooManyRedirects 
import json
import requests



def convert():

    CantidadTo= float(20)
    MonedaFrom= 'EUR' 
    MonedaTo='ETH' 
    API_KEY= 'ff4f88a1-8c9f-4888-8548-c841771b41a3'
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(CantidadTo, MonedaFrom, MonedaTo, API_KEY)
    
    '''
    respuesta = requests.get(url)
    dato = respuesta.json()

    if respuesta.status_code == 200:
        dato = respuesta.json()
    else:
        print ("Se ha producido un error", respuesta.status)
    

    precio = (dato['data']['quote']['EUR']['price'])
    preciounitario = round(form.CantidadFrom.data/precio)

    print (precio)
    print (preciounitario)
    print (precio_u)
    '''



    try:
        response = requests.get(url,params=convert)
        data_2 = json.loads(response.text)
        print(data_2["data"]["quote"]["EUR"]["price"])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

convert()
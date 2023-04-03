import requests
import json
from config import currencys


class ConvertionException(Exception):
    pass

class CryptoConverter(ConvertionException):
    @staticmethod
    def get_price(or_cur, quantity, fin_cur):
        if or_cur == fin_cur:
            raise ConvertionException(f"Введена одна и та же валюта на ввод и вывод: {or_cur}.")

        if or_cur not  in currencys.keys():
            raise ConvertionException(f"Данная валюта '{or_cur}' не поддерживается")
        else:
            or_cur_ticker = currencys[or_cur]

        if fin_cur not in currencys.keys():
            raise ConvertionException(f"Данная валюта '{fin_cur}' не поддерживается")
        else:
            fin_cur_ticker = currencys[fin_cur]

        try:
            quantity = float(quantity)

        except ValueError:
            raise ConvertionException(f'Введено некорректное количество или неподдерживаемый формат количества: {quantity}')

        request = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={or_cur_ticker}&tsyms={fin_cur_ticker}")
        total_fin_cur = json.loads(request.content)[currencys[fin_cur]]
        return total_fin_cur

def get_picture():
    pic = requests.get("https://e7.pngegg.com/pngimages/829/524/png-clipart-currency-foreign-exchange-market-free-content-money-tepid-s-text-logo.png").content
    return pic
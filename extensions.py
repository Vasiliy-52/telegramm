import json
import requests
from bot import dict_


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionException('Введите разные валюты.')
        try:
            quote_ticker = dict_[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')
        try:
            base_ticker = dict_[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество валюты {amount}.')
        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={base_ticker+quote_ticker}'
                         f'&key=0208b9cc054d2edd366e513678aa12d7')
        total_base = json.loads(r.content)
        rez = total_base['data'][base_ticker+quote_ticker]
        cash = float(amount) / float(rez)

        return round(cash, 2)

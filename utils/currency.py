from datetime import date
from pycbrf.toolbox import ExchangeRates


def currency_exchange(currency: str) -> float:
    """ Функция для получения курса выбранной валюты"""
    # Изменение кода валюты для белорусского рубля
    if currency == "BYR":
        currency = "BYN"
    # Получаем текущую дату
    current_date = date.today().strftime('%Y-%m-%d')
    rates = ExchangeRates(current_date)
    result = rates[currency]
    return float(result.rate)

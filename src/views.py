import json
import os
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import read_operations, get_greeting, get_expense, top_five, exchange_rate, read_user_setting, stock_price


#load_dotenv()
#API_KEY = os.getenv("api_key")
#url = f'https://api.twelvedata.com/price?symbol={symbol}&interval=1day&apike'

def main(data_str: str):
    """Функция принимает JSON-ответ и возвращает транзакции с 1-го числа по дату ввода"""
    transactions_df = read_operations("../data/operations.xlsx")
    end_date = pd.to_datetime(data_str, format="%d.%m.%Y")
    start_date = end_date.replace(day=1)

    transactions_df = transactions_df[transactions_df["Дата операции"].between(start_date, end_date)]
    return transactions_df

    print(transactions_df)


#def sort_transactions_by_card(transactions):
 #   """Сортирует транзакции по номеру карты в словарь"""
 #   sorted_transactions = {}
 #   for card_number, amounts in transactions.items():
 #       if card_number in sorted_transactions:
  #          sorted_transactions[card_number].append(amounts)
  #      else:
#            sorted_transactions[card_number] = [amounts]

 #   return sorted_transactions





#def get_mask_card_number(card_number: str) -> str:
 #   """Функция маскировки номера карты"""
 #   card_number = card_number.strip()
 #   if len(card_number) != 16 or not card_number.isdigit():
 #       return "Проверьте номер карты"
 #   last_digits = card_number[-4:]
  #  return f"{last_digits}"


#def get_total_spent():
 #   pass


#def get_top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
 #   """Функция возвращает топ 5 транзакций"""
 #   sorted_transactions = sorted(transactions, key=lambda x: x['amount'])
 #   return sorted_transactions[:5]

#def get_stock_cur(stock: str, yf=None) -> Any:
#    """Функция получает акции с помощью Yahoo Finance"""
#    stock_data = yf.Ticker(stock)
#    todays_data = stock_data.history(period="1d")
#    return todays_data["High"].iloc[0]


#def get_currency_rate(api_key, currency_from, currency_to):
    # URL для получения данных курса валют
#    url = f'https://api.exchangeratesapi.io/latest?access_key={api_key}&format=json&base={currency_from}&symbols={currency_to}'

 #   try:
        # Отправка запроса к API
 #       response = requests.get(url)
  #      response.raise_for_status()  # Проверка на ошибки

        # Преобразование ответа в JSON
 #       data = response.json()

        # Возврат курса валют
  #      return data['rate'][currency_to]
  #  except requests.exceptions.RequestException as e:
  #      print(f"Произошла ошибка при запросе: {e}")
 #       return None

    # Пример использования функции



#api_key = api_key
#currency_from = 'USD'
#currency_to = 'RUB'

#get_currency_rate(api_key, 'USD' , 'RUB')
#if rate:
 #   print(f"Курс {currency_from} к {currency_to} составляет: {rate}")
#else:
 #   print("Не удалось получить курс валют.")


#transactions = {
 #   '123456': [100, 200, 300],
#    '789012': [400, 500],
 #   '123456': [600]
#}

#result = sort_transactions_by_card(transactions)
#print(result)

#rate = get_currency_rates("USD")
#print(rate)

#print(get_stock_cur())

#Генерируем приветствие в зависимости от времени суток
greeting_str = get_greeting()

# Фильтруем данные по указанной дате
filtered_data = main()

# Получаем информацию о расходах по картам
card_expence = get_expense(filtered_data)

# Получаем топ-5 транзакций по сумме
top_five_list = top_five(filtered_data)

# Получаем настройки пользователя для валют и акций
user_currencies = read_user_setting('user_currencies')
user_stocks = read_user_setting('user_stocks')

# Получаем актуальные курсы валют
currency_rates = exchange_rate(user_currencies)

# Получаем актуальные цены акций
stock_prices = stock_price(user_stocks)

result = {
    'greeting': greeting_str,  #Приветствие
    'cards': card_expence, # данные по картам
    'top_transactions': top_five_list, # Топ-5 транзакций
    'currency_rates': currency_rates,  # Курсы валют
    'stock_prices': stock_prices,  # Цены акций
}


main("20.12.2021")

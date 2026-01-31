import json
import os
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import read_operations

load_dotenv()
API_KEY = os.getenv("api_key")


def main(data_str: str):
    """Функция принимает JSON-ответ и возвращает транзакции с 1-го числа по дату ввода"""
    transactions_df = read_operations("../data/operations.xlsx")
    end_date = pd.to_datetime(data_str, format="%d.%m.%Y")
    start_date = end_date.replace(day=1)

    transactions_df = transactions_df[transactions_df["Дата операции"].between(start_date, end_date)]
    print(transactions_df)


def get_greeting(date_time):
    """Функция принимает дату и время и возвращает соответствующее приветствие"""
    dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

    current_hour = dt.hour

    if 5 <= current_hour < 12:
        return "Доброе утро!"
    elif 12 <= current_hour < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


#def group_transactions_by_card(df):
    """Функция возвращает словарь с операциями по каждой карте за данный период"""
    card_transactions = defaultdict(list)
    for card_number, amount in zip(df['card_number'], df['amount']):
        card_transactions[card_number].append(amount)
    return card_transactions



def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера карты"""
    card_number = card_number.strip()
    if len(card_number) != 16 or not card_number.isdigit():
        return "Проверьте номер карты"
    last_digits = card_number[-4:]
    return f"{last_digits}"


def get_total_spent():
    pass


def get_top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция возвращает топ 5 транзакций"""
    sorted_transactions = sorted(transactions, key=lambda x: x['amount'])
    return sorted_transactions[:5]

def get_stock_cur(stock: str, yf=None) -> Any:
    """Функция получает акции с помощью Yahoo Finance"""
    stock_data = yf.Ticker(stock)
    todays_data = stock_data.history(period="1d")
    return todays_data["High"].iloc[0]


def get_currency_rates(currency: str) -> Any:
    """Функция возврщает курс валют"""
    url: str = f"api_url = 'https://api.exchangerate-api.com/v4/latest/RUB'&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
    response_data = json.loads(response.text)
    return response_data["rates"]["RUB"]


get_greeting("2025-08-22 10:30:00")
get_greeting("2025-08-22 15:30:00")
get_greeting("2025-08-22 20:30:00")

get_mask_card_number("7000792289606361")

transactions1 = [{'id': 1, 'amount': 1000},
                 {'id': 2, 'amount': 2000},
                 {'id': 3, 'amount': 1500},
                 {'id': 4, 'amount': 2500},
                 {'id': 5, 'amount': 1200},
                 {'id': 6, 'amount': 1800},
                 {'id': 7, 'amount': 2200},
                 {'id': 8, 'amount': 1300},
                 {'id': 9, 'amount': 2100},
                 {'id': 10, 'amount': 1900}]

get_top_transactions(transactions1)

#group_transactions_by_card(transactions1)

main("20.12.2021")

# Пример использования:
print(get_greeting("2025-08-22 10:30:00"))
print(get_greeting("2025-08-22 15:30:00"))
print(get_greeting("2025-08-22 20:30:00"))

print(get_mask_card_number("7000792289606361"))

print(get_top_transactions(transactions1))

print(get_currency_rates("USD"))

print(get_stock_cur())

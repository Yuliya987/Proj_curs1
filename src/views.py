from typing import List, Dict, Any

from src.utils import read_operations
import pandas as pd
from datetime import datetime
import requests
from collections import defaultdict


def main(data_str: str):
    '''Функция принимает JSON-ответ и возвращает транзакции с 1-го числа по дату ввода'''
    transactions_df = read_operations("../data/operations.xlsx")
    end_date = pd.to_datetime(data_str, format = "%d.%m.%Y")
    start_date = end_date.replace(day=1)

    transactions_df = transactions_df[transactions_df["Дата операции"].between(start_date, end_date)]
    print(transactions_df)


def get_greeting(date_time):
    '''Функция принимает дату и время и возвращает соответствующее приветствие'''
    dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

    current_hour = dt.hour

    if 5 <= current_hour < 12:
        return "Доброе утро!"
    elif 12 <= current_hour < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def group_transactions_by_card(df):
    '''Функция возвращает словарь с операциями по каждой карте за данный период'''
    card_transactions = defaultdict(list)
    for card_number, amount in zip(df['card_number'], df['amount']):
        card_transactions[card_number].append(amount)
        return card_transactions
    print(card_transactions)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера карты."""
    card_number = card_number.strip()
    if len(card_number) != 16 or not card_number.isdigit():
        return "Проверьте номер карты"
    last_digits = card_number[-4:]
    return f"{last_digits}"


def get_total_spent():
    pass


def top_transactions_5(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция возвращает топ 5 транзакций"""
    transactions.sort(key=lambda x: x["transaction_amount"], reverse=True)
    return transactions[:5]


api_url = 'https://api.exchangerate-api.com/v4/latest/RUB'


def get_currency_rates(date_str):
    '''Функция возврщает курс валют'''
    try:
        response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        rates = data['rates']
        currency_rates = {currency: rates[currency] for currency in rates}
        return currency_rates
    else:
        raise Exception(
            f"Ошибка при получении данных: {response.status_code}")
    except requests.exceptions.RequestException as e:
        return f"Ошибка: {str(e)}"


if name == "main":
    date_input = input("Введите дату в формате YYYY-MM-DD: ")
    try: currency_rates = get_currency_rates(date_input)
    print("Курсы валют:")
    for currency, rate in currency_rates.items():
        print(f"{currency}: {rate:.2f} руб.")
    except Exception as e: (
        print(f"Произошла ошибка: {e}"))

get_greeting("2025-08-22 10:30:00")
get_greeting("2025-08-22 15:30:00")
get_greeting("2025-08-22 20:30:00")

group_transactions_by_card(transactions)

get_mask_card_number("7000792289606361")

transactions = [  {'id': 1, 'amount': 1000},
    {'id': 2, 'amount': 2000},
    {'id': 3, 'amount': 1500},
    {'id': 4, 'amount': 2500},
    {'id': 5, 'amount': 1200},
    {'id': 6, 'amount': 1800},
    {'id': 7, 'amount': 2200},
    {'id': 8, 'amount': 1300},
    {'id': 9, 'amount': 2100},
    {'id': 10, 'amount': 1900}   ]

get_top_transactions(transactions)


main("20.12.2021")


# Пример использования:
print(get_greeting("2025-08-22 10:30:00"))
print(get_greeting("2025-08-22 15:30:00"))
print(get_greeting("2025-08-22 20:30:00"))


print(get_mask_card_number("7000792289606361"))


print(get_top_transactions(transactions))

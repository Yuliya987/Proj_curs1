from src.utils import read_operations
import pandas as pd
from datetime import datetime


def main(data_str: str):
    '''Функция принимает JSON-ответ и возвращает транзакции с 1-го числа по дату ввода'''
    df = read_operations("../data/operations.xlsx")
    end_date = pd.to_datetime(data_str, format = "%d.%m.%Y")
    start_date = end_date.replace(day=1)

    df = df[df["Дата операции"].between(start_date, end_date)]
    print(df)


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


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера карты."""
    card_number = card_number.strip()
    if len(card_number) != 16 or not card_number.isdigit():
        return "Проверьте номер карты"
    last_digits = card_number[-4:]
    return f"{last_digits}"


def get_total_spent():
    pass


def get_top_transactions(transactions):
    '''Функция сортирует транзакции по убыванию суммы платежа'''
    sorted_transactions = sorted(transactions, key=lambda x: x['amount'])
    top_transactions = sorted_transactions[:5]
    return top_transactions

get_greeting("2025-08-22 10:30:00")
get_greeting("2025-08-22 15:30:00")
get_greeting("2025-08-22 20:30:00")


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

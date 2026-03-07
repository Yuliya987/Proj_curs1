import json
import os
from datetime import datetime
from functools import wraps
from typing import Any, List, Dict

import logger
import pandas as pd
import logging
from logging import Logger

from dotenv import load_dotenv

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

def read_operations(file_path: str) -> Any:
    """Функция чтения файлов из excel-файлов"""
    transactions_df = pd.read_excel(file_path)

    transactions_df["Дата операции"] = pd.to_datetime(transactions_df["Дата операции"], format = "%d.%m.%Y %H:%M:%S")
    transactions_df["Дата платежа"] = pd.to_datetime(transactions_df["Дата платежа"], format="%d.%m.%Y")

    return transactions_df


def write_json(file_path: str, data: Any) -> None:
    """Запись JSON-файла"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(file_path: str) -> Any:
    """Чтение JSON-файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


logs_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'logs',
)
os.makedirs(logs_path, exist_ok=True)

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(os.path.join(logs_path, 'utils.log'), encoding='utf-8', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Вызов функции {func.__name__}')
        try:
            result = func(*args, **kwargs)
            logger.info(f'Функция {func.__name__} успешно завершилась')
            return result
        except Exception as err:
            logger.error(f"Ошибка в функции {func.__name__}: {str(err)}")
            raise

    return wrapper


@log_function
def get_greeting() -> str | None:
    """Функция возвращает приветствие в зависимости от текущего времени пользователя"""

    # Получаем текущее время
    cur_hour = datetime.now().hour

    # Создаем список приветствий
    greet_message = ['Доброй ночи', 'Доброго утра', 'Доброго дня', 'Доброго вечера']

    # В зависимости от времени выбираем из списка
    time_of_day = cur_hour // 6

    return greet_message[time_of_day]

@log_function
def get_expense(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция для получения суммы трат по картам"""

    # Создаем DataFrame из списка транзакций
    data_frame = pd.DataFrame(data)

    # Проверяем, что DataFrame не пустой и содержит необходимые колонки
    if data_frame.empty or 'amount' not in data_frame.columns or 'card' not in data_frame.columns:
        return []

    # Фильтруем траты (отрицательные суммы), группируем по карте и вычисляем сумму
    expenses = data_frame[data_frame['amount'] < 0].groupby('card')['amount'].sum().abs().round(2)

    # Формируем результат в нужном формате
    result1: List[Dict[str, Any]] = []
    for card, total_amount in expenses.items():
        # Вычисляем кэшбэк 1% от суммы трат
        cashback = round(total_amount * 0.01, 2)
        # Добавляем информацию по карте (последние цифры, сумма трат, кэшбэк)
        result1.append({"last_digits": str(card)[1:], "total_spent": float(total_amount), "cashback": float(cashback)})

    return result1

@log_function
def top_five(data: List[Dict[str, Any]]) -> List[Dict[str, Any]] | None:
    """Функция получает на вход список словарей с транзакциями и возвращает ТОП 5 транзакций по сумме платежа"""

    # Проверяем, что входные данные не пустые
    if not data:
        return None

    # Сортируем транзакции по абсолютному значению суммы (по убыванию) и берем топ-5
    result = sorted(data, key=lambda transaction: abs(transaction.get('amount', 0)), reverse=True)[:5]

    # Форматируем результат для вывода
    formatted_result = []
    for transaction in result:
        formatted_transaction = {}
        # Для каждой транзакции оставляем только нужные поля
        for key in ['date', 'amount', 'category', 'description']:
            if key in transaction:
                if key == 'date':
                    # Для даты оставляем только часть до пробела (убираем время)
                    formatted_transaction[key] = transaction[key].split()[0]
                else:
                    # Для остальных полей копируем как есть
                    formatted_transaction[key] = transaction[key]
        formatted_result.append(formatted_transaction)

    # Возвращаем отформатированный список топ-5 транзакций
    return formatted_result

    #@log_function
#def stock_price(data: List[str]) -> List[Dict[str, Any]] | None:
#        """Функция получает на вход список акций и возвращает список словарей, где ключи - код акций, а значение -
#        стоимость акций"""

    # Инициализируем список для хранения цен акций
 #   stock_prices: List[Dict[str, Any]] = []

    # Загружаем переменные окружения и получаем API ключ
 #   load_dotenv()
 #   api_key = os.getenv('API_KEY')

    # Проверяем наличие API ключа
 #   if not api_key:
 #       logger.error('API_KEY не найден в переменных окружения')
 #   return None

    # Проверяем, что передан непустой список акций
 #   if not data:
 #       logger.warning('Получен пустой список акций')
#    return None

    # Объединяем коды акций в строку через запятую для API запроса
 #   symbol = ','.join(data)

    # Формируем URL для запроса цен акций
 #   url = f'
 #   https: // api.twelvedata.com / price?symbol = {symbol} & interval = 1
  #  day & apikey = {api_key}
   # '

#def get_currency_rate(api_key, currency_from, currency_to):
 #   try:
    # Логируем и выполняем HTTP-запрос к API
 #   logger.info(f'Отправка GET-request для {symbol} на
  #  https: // api.twelvedata.com...
  #  ')

 #   response = requests.get(url, timeout=10)
 #   logger.info(f'Запрос выполнен успешно. Код состояния: {response.status_code}')

    # Проверяем успешность HTTP-запроса
#    if response.status_code != 200:
 #       logger.error(f'API вернул код состояния: {response.status_code} для валюты {symbol}')
 #   return None

    # Парсим JSON ответ от API
#    get_convert = response.json()

    # Обрабатываем данные для каждой акции из исходного списка
#    for stock_symbol in data:
#        if stock_symbol in get_convert:
#            stock_data = get_convert[stock_symbol]
    # Проверяем наличие и валидность цены в ответе
#    if 'price' in stock_data and stock_data['price'] is not None:
#        try:
    # Преобразуем цену в float и добавляем в результат
#    stock_prices.append({'stock': stock_symbol, 'price': float(stock_data['price'])})
 #   logger.info(f'Успешно извлечена цена для {stock_symbol}: {stock_data["price"]}')
 #   except (ValueError, TypeError) as e:
    # Обрабатываем ошибки преобразования типа
    #     logger.error(f"Ошибка преобразования цены для {stock_symbol}: {stock_data['price']} - {e}")
    #     stock_prices.append({'stock': stock_symbol, 'price': None})
  #  else:
    # Логируем отсутствие цены в ответе API
    #     logger.warning(f"Не найдена цена акции {stock_symbol} в ответе: {stock_data}")
    #     stock_prices.append({'stock': stock_symbol, 'price': None})
 #   else:
    # Логируем отсутствие акции в ответе API
    #     logger.warning(f"Акция {stock_symbol} не найдена в ответе API")
    #     stock_prices.append({'stock': stock_symbol, 'price': None})

    # Возвращаем результат или None если список пустой
    return stock_prices if stock_prices else None

    # Обрабатываем ошибки сетевого запроса
 #   except requests.exceptions.RequestException as err:
    #     logger.error(f"При выполнении запроса произошла ошибка: {err}")
    #     return None

    # Обрабатываем ошибки обработки данных
#    except (KeyError, ValueError, TypeError) as err:
    #     logger.error(f"Ошибка при обработке данных для акций {symbol}: {err}")
#     return None
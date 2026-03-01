import json
import os
from datetime import datetime
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


#def loggin() -> Logger:
#    """Настройка логирования для дальнейшего использования в других модулях"""
#    logging.basicConfig(
 #       level=logging.INFO,
#        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
#        filename="utils_log.txt",
#        filemode="w",
 #   )
#    logger = logging.getLogger(__name__)
#    return logger

def read_operations(file_path: str) -> Any:
    """Функция чтения файлов из JSON-файло"""
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
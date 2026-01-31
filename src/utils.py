import json
from typing import Any

import pandas as pd
import logging
from logging import Logger


def loggin() -> Logger:
    """Настройка логирования для дальнейшего использования в других модулях"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        filename="utils_log.txt",
        filemode="w",
    )
    logger = logging.getLogger(__name__)
    return logger

def read_operations(file_path: str) -> Any:
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
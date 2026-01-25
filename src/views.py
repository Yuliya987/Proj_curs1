from src.utils import read_operations
import pandas as pd


def main(data_str: str):

    df = read_operations("../data/operations.xlsx")
    end_date = pd.to_datetime(data_str, format = "%d.%m.%Y")
    start_date = end_date.replace(day=1)

    df = df[df["Дата операции"].between(start_date, end_date)]
    print(df)



main("20.12.2021")
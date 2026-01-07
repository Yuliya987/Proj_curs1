import pandas as pd

def read_operations(file_path):
    df = pd.read_excel(file_path)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format = "%d.%m.%Y %H:%M:%S")
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], format="%d.%m.%Y")

    return df

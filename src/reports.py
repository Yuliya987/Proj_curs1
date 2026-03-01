def decorator_output_to(filename: Optional[str] = None) -> Any:
"""Декоратор для функций-отчетов, записывающий в файл результат (в формате json), который возвращает функция,
формирующая отчет. Декоратор без параметра — записывает данные отчета в файл с названием
имя_декорируемой_функции.json в папку data проекта. Декоратор с параметром — принимает имя файла
в качестве параметра (файл сохраняется также в папку data проекта"""

def decorator(func):
@wraps(func)
def wrapper(*args, **kwargs):
result = func(*args, **kwargs)
json_str = result.to_json(orient='records', indent=2, force_ascii=False)

# Создаем путь к директории вывода файла (два уровня выше от текущего файла)
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
# Создаем директорию, если она не существует
os.makedirs(data_path, exist_ok=True)
# Определяем имя файла для записи
output_filename = (
os.path.join(data_path, filename) if filename else os.path.join(data_path, f"{func.__name__}.json")
)

try:
# Записываем json_result в файл именем output_filename
with open(output_filename, 'w', encoding='utf-8') as f:
f.write(json_str + '\n')

except Exception as e:
# Записываем ошибку в лог
logging.error(f"Ошибка записи в {output_filename}: {e}")
# Программа продолжает работу

return result

return wrapper

return decorator
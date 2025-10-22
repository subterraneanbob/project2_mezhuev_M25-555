from functools import wraps


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок, которые могут возникнуть при выполнении команд.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            table_name = e.args[0] if e.args else e
            print(f'Ошибка: Таблица "{table_name}" не существует.')
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def handle_file_errors(func):
    """
    Декоратор для обработки ошибок при работе с файлами базы данных.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return {}

    return wrapper

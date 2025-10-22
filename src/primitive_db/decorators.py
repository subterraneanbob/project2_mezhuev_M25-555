from functools import wraps

import prompt


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


def confirm_action(action_name: str):
    """
    Декоратор для подтверждения действия пользователем.

    Args:
        action_name (str): Название действия, которое отобразится при подтверждении.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = prompt.character(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/N]: ',
                empty=True,
            )

            if response == "y":
                return func(*args, **kwargs)

        return wrapper

    return decorator

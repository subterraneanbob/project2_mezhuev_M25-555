import json
import os

from .constants import DB_META_FILE, DB_TABLES_DIR, JSON_EXT
from .decorators import handle_file_errors


@handle_file_errors
def load_metadata(filepath: str = DB_META_FILE) -> dict:
    """
    Загружает метаданные о существующих таблицах. Если файл не существует, то
    возвращается пустой словарь.

    Args:
        filepath (str, optional): Путь к файлу с метаданными.
    Returns:
        dict: Словарь, содержащий текущие метаданные.
    """
    with open(filepath, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_metadata(data: dict, filepath: str = DB_META_FILE):
    """
    Сохраняет метаданные в файл.

    Args:
        filepath (str, optional): Путь к файлу с метаданными.
    """
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def _create_table_data_filepath(table_name: str, datapath: str = DB_TABLES_DIR):
    """
    Собирает полный путь к файлу с данными таблицы. Также создаёт директорию, где
    хранятся данные таблицы, если она не существует.
    """
    os.makedirs(datapath, exist_ok=True)
    return os.path.join(datapath, table_name + JSON_EXT)


@handle_file_errors
def load_table_data(table_name: str) -> dict:
    """
    Загружает данные для указанной таблицы.

    Args:
        table_name (str): Название таблицы, данные для которой нужно получить.
    Returns:
        dict: Словарь, содержащий все записи в таблице.
    """
    table_data_path = _create_table_data_filepath(table_name)

    with open(table_data_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_table_data(table_name: str, data: dict):
    """
    Сохраняет данные для указанной таблицы.

    Args:
        table_name (str): Название таблицы, данные для которой нужно сохранить.
        data (dict): Словарь, который содержит все записи в таблице.
    """
    table_data_path = _create_table_data_filepath(table_name)

    with open(table_data_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

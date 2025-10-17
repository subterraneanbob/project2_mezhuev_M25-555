import json

from .constants import DB_META_FILE


def load_metadata(filepath: str = DB_META_FILE) -> dict:
    """
    Загружает метаданные о существующих таблицах. Если файл не существует, то
    возвращается пустой словарь.

    Args:
        filepath (str, optional): Путь к файлу с метаданными.
    Returns:
        dict: Словарь, содержащий текущие метаданные.
    """

    try:
        with open(filepath, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


def save_metadata(data: dict, filepath: str = DB_META_FILE):
    """
    Сохраняет метаданные в файл.

    Args:
        filepath (str, optional): Путь к файлу с метаданными.
    """
    with open(filepath, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

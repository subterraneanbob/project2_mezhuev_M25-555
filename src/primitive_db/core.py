from collections.abc import Iterable

from .constants import ID_COLUMN_DATA_TYPE, ID_COLUMN_NAME, SUPPORTED_DATA_TYPES


def create_table(metadata: dict, table_name: str, columns: Iterable[str]) -> dict:
    """
    Добавляет новую таблицу с указанными столбцами в словарь метаданных, если
    таблицы с таким именем не существует. Столбец "ID:int" будет добавлен
    автоматически.

    Выводит ошибку, если:
    - таблица уже существует
    - указан некорректный тип данных (поддерживаются: int | str | bool)

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название новой таблицы
        columns (Iterable[str]): Список столбцов в виде "название:тип_данных"

    Returns:
        dict: Обновлённый словарь метаданных.
    """

    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_metadata = {ID_COLUMN_NAME: ID_COLUMN_DATA_TYPE}

    for column in columns:
        name, _, data_type = map(str.strip, column.partition(":"))

        if data_type not in SUPPORTED_DATA_TYPES:
            print(f'Некорректное значение: "{column}". Попробуйте снова.')
            return metadata

        # Столбец ID всегда добавляется автоматически, даже если указан явно
        if name == ID_COLUMN_NAME:
            continue

        table_metadata[name] = data_type

    metadata[table_name] = table_metadata

    created_columns = [":".join(item) for item in table_metadata.items()]
    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {', '.join(created_columns)}"
    )

    return metadata


def drop_table(metadata: dict, table_name: str) -> dict:
    """
    Удаляет информацию о таблице из метаданных. Если таблицы не существует,
    выводит ошибку.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы для удаления
    Returns:
        dict: Обновлённый словарь метаданных.
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata

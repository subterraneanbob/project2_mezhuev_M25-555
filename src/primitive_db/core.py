from collections.abc import Iterable

from .constants import (
    ID_COLUMN_DATA_TYPE,
    ID_COLUMN_NAME,
    ID_INITIAL_VALUE,
    SUPPORTED_DATA_TYPES,
)


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

    if not table_name:
        print(f'Ошибка: Недопустимое имя таблицы "{table_name}".')
        return metadata

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


def list_tables(metadata: dict):
    """
    Выводит список существующих таблиц или сообщение о том, что таблиц нет.

    Args:
        metadata (dict): Текущие метаданные
    """

    if metadata:
        print(*[f"- {table}" for table in metadata], sep="\n")
    else:
        print("Таблицы отсутствуют.")


def insert(
    metadata: dict,
    table_name: str,
    table_data: dict,
    values: Iterable[int | str | bool],
) -> dict:
    """
    Добавляет новую запись в таблицу, если она существует. Перед добавлением
    производится проверка значений на соответствие схеме таблицы. Значение для
    ключа таблицы (поле ID) заполняется автоматически.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы
        table_data (dict): Текущие данные таблицы
        values (Iterable[int or str or bool]): Новые значения для добавления
    Returns:
        dict: Обновлённые данные таблицы.
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    table_metadata = metadata[table_name]
    columns = [column for column in table_metadata if column != ID_COLUMN_NAME]

    if len(values) != len(columns):
        print("Ошибка: Передано неверное количество значений.")
        return table_data

    new_entry = dict.fromkeys(columns)
    for i, (value, column) in enumerate(zip(values, columns), start=1):
        type_name = table_metadata[column]
        data_type = SUPPORTED_DATA_TYPES[type_name]
        if not isinstance(value, data_type):
            print(
                f'Ошибка: Неверный тип данных для столбца "{column}" ({i}). '
                f"Ожидается {type_name}."
            )
            return table_data
        new_entry[column] = value

    new_id = (
        max(int(key) for key in table_data.keys()) + 1
        if table_data
        else ID_INITIAL_VALUE
    )
    table_data[new_id] = new_entry

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data

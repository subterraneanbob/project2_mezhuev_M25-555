from collections.abc import Iterable

from prettytable import PrettyTable

from .constants import (
    ID_COLUMN_DATA_TYPE,
    ID_COLUMN_DATA_TYPE_STR,
    ID_COLUMN_NAME,
    ID_INITIAL_VALUE,
    SUPPORTED_DATA_TYPES,
)


def _check_clause(
    metadata: dict, table_name: str, clause: dict, show_column_index: bool = False
) -> bool:
    """
    Проверяет пары {столбец : значение} на соответствие схеме данных таблицы.
    Выводит сообщение при ошибке.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы
        clause (dict): Словарь
        show_column_index (bool, optional): Указывать номер столбца в тексте ошибки
    """
    table_metadata = metadata[table_name]

    for i, (column, value) in enumerate(clause.items(), start=1):
        if column not in table_metadata:
            print(f'Ошибка: Недопустимое имя столбца "{column}".')
            return False

        type_name = table_metadata[column]
        data_type = SUPPORTED_DATA_TYPES[type_name]
        if not isinstance(value, data_type):
            column_index = f"#{i} " if show_column_index else ""
            print(
                f'Ошибка: Неверный тип данных для столбца {column_index}"{column}". '
                f"Ожидается {type_name}."
            )
            return False

    return True


def _filter_ids(table_data: dict, where_clause: dict) -> list:
    """
    Возвращает список первичных ключей, которые удовлетворяют указанному условию.

    Args:
        table_data (dict): Текущие данные таблицы
        where_clause (dict): Условия для фильтрации
    Returns:
        list: Список первичных ключей.
    """
    filtered_keys = []

    for key, data in table_data.items():
        for filter_column, filter_value in where_clause.items():
            if filter_column == ID_COLUMN_NAME:
                # ID хранятся в строковом виде - приводим к корректному типу
                current_value = ID_COLUMN_DATA_TYPE(key)
            else:
                current_value = data[filter_column]

            if current_value != filter_value:
                break
        else:
            filtered_keys.append(key)

    return filtered_keys


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

    table_metadata = {ID_COLUMN_NAME: ID_COLUMN_DATA_TYPE_STR}

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

    new_entry = dict(zip(columns, values))
    if not _check_clause(metadata, table_name, new_entry, show_column_index=True):
        return table_data

    new_id = (
        max(ID_COLUMN_DATA_TYPE(key) for key in table_data.keys()) + 1
        if table_data
        else ID_INITIAL_VALUE
    )
    table_data[new_id] = new_entry

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data


def select(
    metadata: dict,
    table_name: str,
    table_data: dict,
    where_clause: dict = None,
):
    """
    Выводит все записи из данных таблицы. Если указано условие where_clause, то
    записи фильтруются и выводятся только подходящие.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы
        table_data (dict): Текущие данные таблицы
        where_clause (dict or None): Условия для фильтрации (если применимы)
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    where_clause = where_clause or {}
    if not _check_clause(metadata, table_name, where_clause):
        return

    table = PrettyTable()
    table.field_names = list(metadata[table_name].keys())

    for key in _filter_ids(table_data, where_clause):
        table.add_row([key, *table_data[key].values()])

    print(table)


def update(
    metadata: dict,
    table_name: str,
    table_data: dict,
    set_clause: dict,
    where_clause: dict,
) -> dict:
    """
    Обновляет существующие записи в указанной таблице, выбирая их по условию.
    Если попытаться обновить первичный ключ, выводит ошибку.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы
        table_data (dict): Текущие данные таблицы
        set_clause (dict): Столбцы, которые нужно обновить, со значениями
        where_clause (dict): Условия для выбора записей для обновления.
    Returns:
        dict: Обновлённые данные таблицы.
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    if ID_COLUMN_NAME in set_clause:
        print(f"Ошибка: значение первичного ключа {ID_COLUMN_NAME} нельзя обновить.")
        return table_data

    if any(
        not _check_clause(metadata, table_name, clause)
        for clause in (set_clause, where_clause)
    ):
        return table_data

    for key in _filter_ids(table_data, where_clause):
        table_data[key] |= set_clause
        print(f'Запись с ID={key} в таблице "{table_name}" успешно обновлена.')

    return table_data


def delete(
    metadata: dict,
    table_name: str,
    table_data: dict,
    where_clause: dict,
) -> dict:
    """
    Удаляет записи из указанной таблицы по условию.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы
        table_data (dict): Текущие данные таблицы
        where_clause (dict): Условия для выбора записей для обновления.
    Returns:
        dict: Обновлённые данные таблицы.
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    if not _check_clause(metadata, table_name, where_clause):
        return table_data

    for key in _filter_ids(table_data, where_clause):
        del table_data[key]
        print(f'Запись с ID={key} успешно удалена из таблицы "{table_name}".')

    return table_data


def info(metadata: dict, table_name: str, table_data: dict):
    """
    Выводит информацию о таблице: название, схема данных (колонки и типы данных),
    количество записей.

    Args:
        metadata (dict): Текущие метаданные
        table_name (str): Название таблицы
        table_data (dict): Текущие данные таблицы
    """

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_metadata = metadata[table_name]
    columns = ", ".join(
        f"{column}:{data_type}" for column, data_type in table_metadata.items()
    )

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns}")
    print(f"Количество записей: {len(table_data)}")

from collections.abc import Callable

import prompt

from .constants import (
    DATA_COMMANDS_REFERENCE,
    OTHER_COMMANDS_REFERENCE,
    TABLE_COMMANDS_REFERENCE,
    Command,
)
from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from .decorators import create_cacher
from .parser import parse_command
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def _save_metadata_when_modified(
    table_name: str, new_metadata: dict | None, cache_invalidator: Callable
):
    """
    Сохраняет метаданные, удаляет данные из таблицы и очищает кэш,
    если новое значение метаданных не None.

    Args:
        table_name (str): Название таблицы
        metadata (dict, optional): Обновлённые метаданные или None
        cache_invalidator (Callable): Функция очистки кэша
    """
    if new_metadata is not None:
        save_metadata(new_metadata)
        save_table_data(table_name, {})  # Удаляем все данные таблицы
        cache_invalidator()


def _save_data_when_modified(
    table_name: str, new_table_data: dict | None, cache_invalidator: Callable
):
    """
    Сохраняет данные таблицы и очищает кэш, если новое значение не None.

    Args:
        table_name (str): Название таблицы
        table_data (dict, optional): Обновлённые данные таблицы или None
        cache_invalidator (Callable): Функция очистки кэша
    """
    if new_table_data is not None:
        save_table_data(table_name, new_table_data)
        cache_invalidator()


def get_command_from_user() -> str:
    """
    Запрашивает команду у пользователя и возвращает её в виде строки.

    Returns:
        str: Пользовательская команда.
    """

    try:
        return prompt.string("\nВведите команду: ")
    except (KeyboardInterrupt, EOFError):
        return Command.EXIT


def print_help():
    """Печатает справочную информацию по работе с программой."""

    print("\nКоманды для операций с данными:")
    for command, description in DATA_COMMANDS_REFERENCE:
        print(f"<command> {command} - {description}")

    print("\nКоманды для работы с таблицами:")
    for command, description in TABLE_COMMANDS_REFERENCE:
        print(f"<command> {command} - {description}")

    print("\nОбщие команды:")
    for command, description in OTHER_COMMANDS_REFERENCE:
        print(f"<command> {command} - {description}")


def run():
    """
    Выполняет основной цикл программы: запрашивает команду у пользователя и
    выполняет её.
    """

    print_help()

    cacher = create_cacher()
    cache_invalidator = cacher.invalidate

    while True:
        cmd = get_command_from_user()
        metadata = load_metadata()

        match parse_command(cmd):
            case (Command.INFO, table_name):
                table_data = load_table_data(table_name)
                info(metadata, table_name, table_data)
            case (Command.DELETE, table_name, where_clause):
                table_data = load_table_data(table_name)
                new_table_data = delete(metadata, table_name, table_data, where_clause)
                _save_data_when_modified(table_name, new_table_data, cache_invalidator)
            case (Command.UPDATE, table_name, set_clause, where_clause):
                table_data = load_table_data(table_name)
                new_table_data = update(
                    metadata, table_name, table_data, set_clause, where_clause
                )
                _save_data_when_modified(table_name, new_table_data, cache_invalidator)
            case (Command.SELECT, table_name, where_clause):
                table_data = load_table_data(table_name)
                select(metadata, table_name, table_data, where_clause, cacher)
            case (Command.INSERT, table_name, values):
                table_data = load_table_data(table_name)
                new_table_data = insert(metadata, table_name, table_data, values)
                _save_data_when_modified(table_name, new_table_data, cache_invalidator)
            case (Command.CREATE_TABLE, table_name, columns):
                new_metadata = create_table(metadata, table_name, columns)
                _save_metadata_when_modified(
                    table_name, new_metadata, cache_invalidator
                )
            case (Command.DROP_TABLE, table_name):
                new_metadata = drop_table(metadata, table_name)
                _save_metadata_when_modified(
                    table_name, new_metadata, cache_invalidator
                )
            case Command.LIST_TABLES:
                list_tables(metadata)
            case Command.HELP:
                print_help()
            case Command.EXIT:
                break
            case None:
                print("Синтаксическая ошибка. Проверьте правильность команды.")
            case unknown_cmd:
                print(f'Функции "{unknown_cmd}" нет. Попробуйте снова.')

import prompt

from .constants import DATA_COMMANDS, OTHER_COMMANDS, TABLE_COMMANDS, Command
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
from .parser import parse_command
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


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
    for command, description in DATA_COMMANDS.items():
        print(f"<command> {command} - {description}")

    print("\nКоманды для работы с таблицами:")
    for command, description in TABLE_COMMANDS.items():
        print(f"<command> {command} - {description}")

    print("\nОбщие команды:")
    for command, description in OTHER_COMMANDS.items():
        print(f"<command> {command} - {description}")


def run():
    """
    Выполняет основной цикл программы: запрашивает команду у пользователя и
    выполняет её.
    """

    print_help()

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
                save_table_data(table_name, new_table_data)
            case (Command.UPDATE, table_name, set_clause, where_clause):
                table_data = load_table_data(table_name)
                new_table_data = update(
                    metadata, table_name, table_data, set_clause, where_clause
                )
                save_table_data(table_name, new_table_data)
            case (Command.SELECT, table_name, where_clause):
                table_data = load_table_data(table_name)
                select(metadata, table_name, table_data, where_clause)
            case (Command.INSERT, table_name, values):
                table_data = load_table_data(table_name)
                new_table_data = insert(metadata, table_name, table_data, values)
                save_table_data(table_name, new_table_data)
            case (Command.CREATE_TABLE, table_name, columns):
                create_table(metadata, table_name, columns)
                save_metadata(metadata)
            case (Command.DROP_TABLE, table_name):
                drop_table(metadata, table_name)
                save_metadata(metadata)
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

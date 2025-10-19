import prompt

from .constants import OTHER_COMMANDS, TABLE_COMMANDS, Command
from .core import create_table, drop_table, list_tables
from .parser import parse_command
from .utils import load_metadata, save_metadata


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

import shlex

import prompt

from .constants import (
    CREATE_TABLE,
    DROP_TABLE,
    EXIT,
    HELP,
    LIST_TABLES,
    OTHER_COMMANDS,
    TABLE_COMMANDS,
)
from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


class ParsedCommand:
    """
    Разбирает команду на составные части: первая часть - это имя команды,
    остальные - аргументы.
    """

    def __init__(self, command_text: str):
        try:
            self.parts = shlex.split(command_text)
        except ValueError:
            self.parts = []

    def __getitem__(self, key: int | slice):
        if isinstance(key, slice):
            return self.parts[key]

        if -len(self.parts) <= key < len(self.parts):
            return self.parts[key]

        return ""

    def __eq__(self, value) -> bool:
        if isinstance(value, str):
            return self.command == value

        if isinstance(value, ParsedCommand):
            return self.parts == value.parts

        return False

    def __str__(self) -> str:
        return self.command

    def __repr__(self) -> str:
        return f'UserInput("{" ".join(self.parts)}")'

    @property
    def command(self) -> str:
        return self[0]

    @property
    def first_arg(self) -> str:
        return self[1]

    @property
    def args(self) -> list[str]:
        return self[1:]


def get_command_from_user() -> ParsedCommand:
    """
    Запрашивает команду у пользователя и возвращает её в виде объекта
    ParsedCommand.

    Returns:
        ParsedCommand: Пользовательская команда в виде
            компонентов: команды и аргументов.
    """

    try:
        user_input = prompt.string("Введите команду: ")
        return ParsedCommand(user_input)
    except (KeyboardInterrupt, EOFError):
        return ParsedCommand(EXIT)


def print_help():
    """Печатает справочную информацию по работе с программой."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    for command, description in TABLE_COMMANDS.items():
        print(f"<command> {command} - {description}")

    print("\nОбщие команды:")
    for command, description in OTHER_COMMANDS.items():
        print(f"<command> {command} - {description}")
    print()


def run():
    """
    Выполняет основной цикл программы: запрашивает команду у пользователя и
    выполняет её.
    """

    print("***База данных***")
    print_help()

    while (cmd := get_command_from_user()) != EXIT:
        metadata = load_metadata()

        if cmd == CREATE_TABLE:
            create_table(metadata, cmd.first_arg, cmd.args[1:])
            save_metadata(metadata)
        elif cmd == DROP_TABLE:
            drop_table(metadata, cmd.first_arg)
            save_metadata(metadata)
        elif cmd == LIST_TABLES:
            list_tables(metadata)
        elif cmd == HELP:
            print_help()
        else:
            print(f'Функции "{cmd}" нет. Попробуйте снова.')

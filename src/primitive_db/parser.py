import shlex
from typing import Optional

from .constants import Command


def _is_unknown(cmd: str) -> bool:
    return cmd not in (
        Command.HELP,
        Command.EXIT,
        Command.LIST_TABLES,
        Command.DROP_TABLE,
        Command.CREATE_TABLE,
    )


def parse_command(user_input: str) -> Optional[str | tuple]:
    """
    Превращает строку, введённую пользователем, в команду с определёнными
    набором параметров (или без них). Возвращает кортеж из команды и параметров,
    или только название команды, если параметров не предусмотрено.

    В случае синтаксической ошибки возвращается None, а если команда неизвестна,
    то только её имя.

    Args:
        user_input (str): Строка ввода от пользователя.
    Returns:
        Optional[str | tuple]: Кортеж из команды и параметров, только команда или None.
    """

    tokens = shlex.split(user_input)

    match tokens:
        case [Command.HELP | Command.EXIT | Command.LIST_TABLES as cmd, *_]:
            return cmd
        case [Command.DROP_TABLE as cmd, table_name, *_]:
            return cmd, table_name
        case [Command.CREATE_TABLE as cmd, table_name, *columns]:
            return cmd, table_name, columns
        case [cmd, *_]:
            return cmd if _is_unknown(cmd) else None
        case _:
            return ""

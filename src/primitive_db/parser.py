import shlex
from typing import Optional

from .constants import PLUS_MINUS, Bool, Command, Keyword


def _is_unknown(cmd: str) -> bool:
    """
    Проверяет, является ли команда неизвестной.

    Args:
        cmd (str): Название команды
    Returns:
        bool: True, если команда неизвестна, иначе False.
    """
    return cmd not in (
        Command.HELP,
        Command.EXIT,
        Command.LIST_TABLES,
        Command.DROP_TABLE,
        Command.CREATE_TABLE,
        Command.INSERT,
        Command.SELECT,
        Command.UPDATE,
        Command.DELETE,
        Command.INFO,
    )


def _as_bool(token: str) -> Optional[bool]:
    """
    Конвертирует литералы true/false в тип данных bool.

    Args:
        token (str): Строка для конвертации в bool.
    Returns:
        bool or None: Строка "true" будет конвертирована в True, "false" - в False,
            иначе возвращается None.
    """
    match token:
        case Bool.TRUE:
            return True
        case Bool.FALSE:
            return False


def _as_int(token: str) -> Optional[int]:
    """
    Конвертирует строку, состоящую из цифр и знака + или -, в тип данных int.

    Args:
        token (str): Строка для конвертации в int.
    Returns:
        int or None: Значение типа int, если удалось конвертировать, None - если нет.
    """
    try:
        return int(token)
    except ValueError:
        return None


def _as_str(token: str, quote_char: str) -> Optional[str]:
    """
    Возвращает текст из кавычек, если начальное значение было заключено в них.
    Символ кавычек указывается параметром.

    Args:
        token (str): Строка для преобразования.
    Returns:
        str or None: Текст из кавычек или None, если текст был без кавычек.
    """
    if token.startswith(quote_char) and token.endswith(quote_char):
        return token[1:-1]


def _convert_token(token: str) -> Optional[int | str | bool]:
    """
    Преобразует токен в тип данных Python (поддерживаются int, str, bool) по
    следующим правилам:
    - true, false преобразуются в True, False
    - строки типа 123, +456, -789 преобразуются в int
    - из строк, заключённых в кавычки (двойные или одинарные), извлекается текст
    - для остальных строк возвращается None

    Args:
        token (str): Токен для преобразования.
    Returns:
        int or str or bool or None: Тип данных согласно правилам или None, если
            преобразование не удалось.
    """
    if not token:
        return None

    match token[0]:
        case ch if ch in (Bool.TRUE[0], Bool.FALSE[0]):
            return _as_bool(token)
        case ch if ch.isdigit() or ch in PLUS_MINUS:
            return _as_int(token)
        case '"' | "'" as quote_ch:
            return _as_str(token, quote_ch)


def _tokenize(user_input: str) -> Optional[list[str]]:
    """
    Разбивает входную строку на токены.

    Args:
        user_input (str): Строка для разбивки.
    Returns:
        list[str] or None: Возвращает список токенов или None, если строку не
            получается разобрать (при ошибках синтаксиса).
    """
    try:
        lexer = shlex.shlex(user_input, posix=False)
        lexer.wordchars += PLUS_MINUS
        return list(lexer)
    except ValueError:
        return None


def _parse_values_clause(user_input: str) -> Optional[list[str]]:
    """
    Извлекает значения для вставки из команд типа "insert into <имя_таблицы> values
    (<значение1>, <значение2>, ...)".

    Args:
        user_input (str): Команда для обработки.
    Returns:
        list[str] or None: Возвращает список значений или None, если строку не
            получается разобрать (при ошибках синтаксиса).
    """

    # Извлекаем токены в скобках
    value_tokens = []
    match _tokenize(user_input):
        case [_, _, _, Keyword.VALUES, "(", *value_tokens, ")"]:
            pass
        case _:
            return None

    # Должно получиться нечётное или нулевое кол-во токенов (значения и запятые)
    if value_tokens and len(value_tokens) % 2 == 0:
        return None

    # Проверяем, на месте ли запятые (нечётные позиции)
    if any(token != "," for token in value_tokens[1::2]):
        return None

    # Конвертируем значения из строк в типы данных Python
    result = []
    for token in value_tokens[0::2]:
        if (value := _convert_token(token)) is None:
            return None
        result.append(value)

    return result


def _parse_where_clause(user_input: str) -> Optional[dict]:
    """
    Извлекает значения для фильтрации данных из команд типа
    "select from <имя_таблицы> where <столбец> = <значение>".

    Args:
        user_input (str): Команда для обработки.
    Returns:
        dict or None: Возвращает словарь {столбец : значение} или None при
            ошибках синтаксиса.
    """
    match _tokenize(user_input):
        case [*_, Keyword.WHERE, column, "=", raw_value]:
            if (value := _convert_token(raw_value)) is not None:
                return {column: value}
        case _:
            return None


def _parse_set_clause(user_input: str) -> Optional[dict]:
    """
    Извлекает значения для обновления данных из команд типа "update <имя_таблицы>
    set <столбец> = <новое_значение> where <столбец_условия> = <значение_условия>".

    Args:
        user_input (str): Команда для обработки.
    Returns:
        dict or None: Возвращает словарь {столбец : значение} или None при
            ошибках синтаксиса.
    """
    match _tokenize(user_input):
        case [_, _, Keyword.SET, column, "=", raw_value, *_]:
            if (value := _convert_token(raw_value)) is not None:
                return {column: value}
        case _:
            return None


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

    try:
        tokens = shlex.split(user_input)
    except ValueError:
        return None

    match tokens:
        case [Command.HELP | Command.EXIT | Command.LIST_TABLES as cmd, *_]:
            return cmd
        case [Command.DROP_TABLE as cmd, table_name, *_]:
            return cmd, table_name
        case [Command.CREATE_TABLE as cmd, table_name, *columns]:
            return cmd, table_name, columns
        case [Command.INSERT as cmd, Keyword.INTO, table_name, *_]:
            if (values := _parse_values_clause(user_input)) is not None:
                return cmd, table_name, values
        case [Command.SELECT as cmd, Keyword.FROM, table_name]:
            return cmd, table_name, None
        case [Command.SELECT as cmd, Keyword.FROM, table_name, *_]:
            if (where_clause := _parse_where_clause(user_input)) is not None:
                return cmd, table_name, where_clause
        case [Command.UPDATE as cmd, table_name, *_]:
            if (set_clause := _parse_set_clause(user_input)) is not None:
                if (where_clause := _parse_where_clause(user_input)) is not None:
                    return cmd, table_name, set_clause, where_clause
        case [Command.DELETE as cmd, Keyword.FROM, table_name, *_]:
            if (where_clause := _parse_where_clause(user_input)) is not None:
                return cmd, table_name, where_clause
        case [Command.INFO as cmd, table_name]:
            return cmd, table_name
        case [cmd, *_]:
            return cmd if _is_unknown(cmd) else None
        case _:
            return ""

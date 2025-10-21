# Файлы для хранения состояния базы данных
DB_META_FILE = "db_meta.json"
DB_TABLES_DIR = "data"
JSON_EXT = ".json"

# Доступные типы данных
SUPPORTED_DATA_TYPES = {"int": int, "str": str, "bool": bool}

# Первичный ключ
ID_COLUMN_NAME = "ID"
ID_COLUMN_DATA_TYPE_STR = "int"
ID_COLUMN_DATA_TYPE = SUPPORTED_DATA_TYPES[ID_COLUMN_DATA_TYPE_STR]
ID_INITIAL_VALUE = 1


# Доступные команды
class Command:
    # Команды для работы с данными
    INSERT = "insert"
    SELECT = "select"
    UPDATE = "update"
    DELETE = "delete"
    # Команды для управления таблицами
    CREATE_TABLE = "create_table"
    LIST_TABLES = "list_tables"
    DROP_TABLE = "drop_table"
    # Общие команды
    EXIT = "exit"
    HELP = "help"


# Ключевые слова, которые используются в командах
class Keyword:
    INTO = "into"
    VALUES = "values"
    FROM = "from"
    WHERE = "where"
    SET = "set"


# Литералы истина/ложь
class Bool:
    TRUE = "true"
    FALSE = "false"


PLUS_MINUS = "+-"

DATA_COMMANDS = {
    f"{Command.INSERT} {Keyword.INTO} <имя_таблицы> {Keyword.VALUES} "
    "(<значение1>, <значение2>, ...)": "создать запись",
    f"{Command.SELECT} {Keyword.INTO} <имя_таблицы> {Keyword.WHERE}"
    " <столбец> = <значение>": "прочитать записи по условию",
    f"{Command.SELECT} {Keyword.INTO} <имя_таблицы>": "прочитать все записи",
    f"{Command.UPDATE} <имя_таблицы> {Keyword.SET} <столбец> = <новое_значение> "
    f"{Keyword.WHERE} <столбец_условия> = <значение_условия>": "обновить запись",
    f"{Command.DELETE} {Keyword.FROM} <имя_таблицы> {Keyword.WHERE} "
    "<столбец> = <значение>": "удалить запись",
}

TABLE_COMMANDS = {
    (
        f"{Command.CREATE_TABLE} <имя_таблицы> <столбец1:тип> <столбец2:тип> .."
    ): "создать таблицу",
    f"{Command.DROP_TABLE} <имя_таблицы>": "удалить таблицу",
    Command.LIST_TABLES: "показать список всех таблиц",
}

OTHER_COMMANDS = {
    Command.EXIT: "выход из программы",
    Command.HELP: "справочная информация",
}

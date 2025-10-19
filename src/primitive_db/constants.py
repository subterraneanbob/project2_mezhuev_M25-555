DB_META_FILE = "db_meta.json"
DB_TABLES_DIR = "data"
JSON_EXT = ".json"

ID_COLUMN_NAME = "ID"
ID_COLUMN_DATA_TYPE = "int"

# Доступные типы данных
SUPPORTED_DATA_TYPES = ("int", "str", "bool")


# Доступные команды
class Command:
    # Команды для управления таблицами
    CREATE_TABLE = "create_table"
    LIST_TABLES = "list_tables"
    DROP_TABLE = "drop_table"
    # Общие команды
    EXIT = "exit"
    HELP = "help"


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

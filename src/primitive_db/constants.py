DB_META_FILE = "db_meta.json"
DB_TABLES_DIR = "data"
JSON_EXT = ".json"

ID_COLUMN_NAME = "ID"
ID_COLUMN_DATA_TYPE = "int"

# Доступные типы данных
SUPPORTED_DATA_TYPES = ("int", "str", "bool")

# Команды для управления таблицами
CREATE_TABLE = "create_table"
LIST_TABLES = "list_tables"
DROP_TABLE = "drop_table"

TABLE_COMMANDS = {
    f"{CREATE_TABLE} <имя_таблицы> <столбец1:тип> <столбец2:тип> ..": "создать таблицу",
    f"{DROP_TABLE} <имя_таблицы>": "удалить таблицу",
    LIST_TABLES: "показать список всех таблиц",
}

# Общие команды
EXIT = "exit"
HELP = "help"

OTHER_COMMANDS = {
    EXIT: "выход из программы",
    HELP: "справочная информация",
}

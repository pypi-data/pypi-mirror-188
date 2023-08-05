from typing import Final
from random import randrange


# @ref https://stackoverflow.com/questions/9108833/postgres-autoincrement-not-updated-on-explicit-id-inserts
def reset_max_id_for_series(schema: str, table: str, col: str, cursor):
    cursor.execute(f"SELECT setval('{table}_{col}_seq', (SELECT MAX({col}) FROM \"{schema}.{table}\"));")


Min_DB_Id_Series: Final = 100000
MIN_TEST_Id_Series: Final = 10000
MAX_TEST_Id_Series: Final = 20000


# @ref https://www.postgresql.org/docs/current/functions-sequence.html
def set_max_id_for_serial_column(schema: str, table: str, col: str, cursor, min_id=Min_DB_Id_Series):
    cursor.execute(f"SELECT setval(pg_get_serial_sequence('"
                   f"{schema}.{table}', '{col}'), "
                   f"{min_id + randrange(int(min_id/10))}, true);")

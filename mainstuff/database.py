import os
import sqlite3

# def load_banners():
#     return 0


# def load_user_settings():
#     return 0


global schema_file
schema_file = 'mainstuff/schema.sql'


def check_db(filename: str) -> bool:
    return os.path.exists(filename)


def get_tables(conn: sqlite3.Connection) -> list[str]:
    cur = conn.cursor()
    tables = []
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cur.fetchall()
    for row in rows:
        tables.append(row)
    tables = [tab[0] for tab in tables]
    return tables


def check_table(table: str, conn:  sqlite3.Connection) -> bool:
    tables = get_tables(conn)
    if table in tables:
        return True
    else:
        return False


def create_data_tables(schema_filepath, conn: sqlite3.Connection) -> int:
    # TODO FIX THIS AND HAVE A BETTER GLOBAL VARIABLE FOR IT OR SOMETHING
    if schema_filepath == "":
        schema_filepath = "C:\\Users\\carol\\Code\\Personal\\GenshinWishOracle\\mainstuff\\schema.sql"
    # will only create each table if it doesn't exist
    with open(schema_filepath, 'r') as rf:
        # Read the schema from the file
        schema = rf.read()
        conn.executescript(schema)
    return 0


def init_db(conn: sqlite3.Connection) -> int:
    create_data_tables("", conn)
    # TODO Make init generate analytical data for characters and weapons
    return 0


def get_default_db() -> str:
    return "database.db"


def update_data_in_table(data: list[tuple], table: str, conn: sqlite3.Connection) -> int:
    cur = conn.cursor()
    question_marks = "?, "*len(data[0])
    question_marks = question_marks[0:len(question_marks)-2]
    cur.executemany("INSERT OR REPLACE INTO {} VALUES({})".format(
        table, question_marks), data)
    conn.commit()
    return 0


def print_table(table: str, conn: sqlite3.Connection) -> None:
    i = 0
    cur = conn.cursor()
    cur.execute("SELECT * FROM {};".format(table))
    rows = cur.fetchall()
    for row in rows:
        print(row)
        i += 1


def clear_table(table: str, conn: sqlite3.Connection) -> int:
    cur = conn.cursor()
    cur.execute("DELETE FROM {}".format(
        table),)
    # cur.execute("VACUUM")
    conn.commit()
    return 0


def table_data_to_hashtable(table: str, conn: sqlite3.Connection) -> dict:
    # the first data column (in this case all should be primary keys) becomes the keys for the rest of the data which is stored in a list
    # with the primary key as the key
    cur = conn.cursor()
    hashtable = {}
    cur.execute("SELECT * FROM {}".format(table))
    rows = cur.fetchall()
    for row in rows:
        temp = list(row)
        key = temp.pop(0)
        hashtable[key] = temp
    return hashtable


def get_primary_keys(table: str, conn: sqlite3.Connection) -> list:
    primary_key_column_name = get_primary_key_column_name(table, conn)
    cur = conn.cursor()
    keys = []
    cur.execute("SELECT {} FROM {}".format(primary_key_column_name, table))
    rows = cur.fetchall()
    for prim_key in rows:
        prim_key = prim_key[0]
        keys.append(prim_key)
    return keys


def get_primary_key_column_name(table: str, conn: sqlite3.Connection) -> list:
    cur = conn.cursor()
    cur.execute("PRAGMA table_info({})".format(table))
    rows = cur.fetchall()
    for row in rows:
        if row[5] == 1:
            return row[1]


def get_db_connection(db_file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_file)
    return conn


def reset_database(db_file: str) -> int:

    if check_db(db_file):
        with sqlite3.connect(db_file) as conn:
            tables = get_tables(conn)
            for table in tables:
                clear_table(table, conn)

    with sqlite3.connect(db_file) as conn:
        create_data_tables("", conn)
    return 0


def main():
    global schema_file
    schema_file = 'schema.sql'
    db_file = get_default_db()
    conn = sqlite3.connect(db_file)
    with conn:
        init_db(conn)


if __name__ == "__main__":
    main()

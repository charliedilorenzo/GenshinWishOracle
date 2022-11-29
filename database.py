import os
import sqlite3

# def load_banners():
#     return 0


# def load_user_settings():
#     return 0


global schema_file
schema_file = 'schema.sql'


def check_db(filename: str) -> bool:
    return os.path.exists(filename)


def get_tables(db_file: str) -> list[str]:
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        tables = []
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            tables.append(row)
    return tables


def check_table(conn:  sqlite3.Connection, table: str) -> bool:
    get_tables()


def create_data_tables(conn: sqlite3.Connection) -> int:
    # will only create each table if it doesn't exist
    with open(schema_file, 'r') as rf:
        # Read the schema from the file
        schema = rf.read()
        conn.executescript(schema)
    return 0


def init_db(conn: sqlite3.Connection) -> int:
    create_data_tables(conn)
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


def print_table(table: str, db_file: str) -> int:
    i = 0
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        for row in cur.execute("SELECT * FROM {};".format(table)):
            print(row)
            i += 1
            if i > 1000:
                return 0
    return 0


def clear_table(table: str, db_file: str) -> int:
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM {}".format(
            table),)
        # cur.execute("VACUUM")
        conn.commit()
    return 0


def table_data_to_hashtable(table: str, db_file: str) -> dict:
    # the first data column (in this case all should be primary keys) becomes the keys for the rest of the data which is stored in a list
    # with the primary key as the key
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        hashtable = {}
        for row in cur.execute("SELECT * FROM {}".format(table)):
            temp = list(row)
            key = temp.pop(0)
            hashtable[key] = temp
    return hashtable


def get_db_connection(db_file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_file)
    return conn


def reset_database(db_file: str):
    os.remove(db_file)
    with sqlite3.connect(db_file) as conn:
        create_data_tables(conn)
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

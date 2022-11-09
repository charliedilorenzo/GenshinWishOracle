import os
import sqlite3
import analytical


def check_db(filename):
    return os.path.exists(filename)


def store_percentage_breakdown(filename, breakdown):
    return 0


def add_data_to_table(data, table, conn):
    cur = conn.cursor()
    question_marks = "?, "*len(data[0])
    question_marks = question_marks[0:len(question_marks)-2]
    cur.executemany("INSERT INTO {} VALUES({})".format(
        table, question_marks), data)
    conn.commit()
    return 0


def clear_table(table, db_file="database.db"):
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM {}".format(
            table),)
        cur.execute("VACUUM")
        conn.commit()
    return 0


def create_data_tables(conn):
    with open(schema_file, 'r') as rf:
        # Read the schema from the file
        schema = rf.read()
        conn.executescript(schema)
    return 0


def get_db_connection(database_name="database.db"):
    conn = sqlite3.connect(database_name)
    return conn


def reset_database(database_name="database.db"):
    os.remove(database_name)
    with sqlite3.connect(database_name) as conn:
        create_data_tables(conn)
    return 0


def add_all_analytical_to_db():
    analytical_object = analytical.AnalyticalRecursiveTest(
        "recursive_version_test.csv", {})
    analytical_object.calculate_and_write_all_solutions()

    # converting to sets now
    analytical_sets = []
    hashtable = analytical_object.hashtable
    for key in hashtable.keys():
        current_list = [key]
        for i in range(0, len(hashtable[key])):
            current_list.append(hashtable[key][i])
        current_list = tuple(current_list)
        analytical_sets.append(current_list)

    with sqlite3.connect(db_file) as conn:
        add_data_to_table(
            analytical_sets, "analytical_solutions_character", conn)

    return 0


db_file = 'database.db'
schema_file = 'schema.sql'


# os.remove(db_file)

# if check_db(db_file):
#     with sqlite3.connect(db_file) as conn:
#         cur = conn.cursor()

#         for row in cur.execute("SELECT rateup_five_star, rateup_four_star1 FROM character_banners"):
#             print(row)
#     print('Database already exists. Exiting...')
#     exit(0)

# reset_database()
table = "analytical_solutions_character"
clear_table(table)

add_all_analytical_to_db()

with sqlite3.connect(db_file) as conn:
    create_data_tables(conn)
    cur = conn.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")

    table = "character_banners"
    # data = [("Cool Name", "x86", "1132")]
    # data = [("Baizhu Best Banner", "Baizhu", "Xiangling", "Bennett", "Razor")]
    # data = [("Baizhu Other Banner", "Baizhu", "hello", "Bennett", "Razor")]

    # add_data_to_table(data, table, conn)

    # for row in cur.execute("SELECT rateup_five_star, rateup_four_star1 FROM character_banners"):
    #     print(row)

    i = 0
    for row in cur.execute("SELECT lookup, X, C0, C1, C2, C3, C4, C5, C6 FROM analytical_solutions_character"):
        print(row)
        if i > 1000:
            break
        i += 1

# if check_db(db_file):
#     print('Database already exists. Exiting...')
#     exit(0)

# with open(schema_file, 'r') as rf:
#     # Read the schema from the file
#     schema = rf.read()

# with sqlite3.connect(db_file) as conn:
#     print('Created the connection!')
#     # Execute the SQL query to create the table
#     conn.executescript(schema)
#     print('Created the Table! Now inserting')
#     conn.executescript("""
#                        insert into images (name, size, date)
#                        values
#                        ('sample.png', 100, '2019-10-10'),
#                        ('ask_python.png', 450, '2019-05-02'),
#                        ('class_room.jpeg', 1200, '2018-04-07');
#                        """)
#     print('Inserted values into the table!')
# print('Closed the connection!')

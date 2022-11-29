from analytical import AnalyticalRecursiveTest
import database
import sqlite3

db_file = database.get_default_db()

conn = database.get_db_connection(db_file)
database.create_data_tables(conn)

tables = database.get_tables(db_file)
tables = [tables[i][0] for i in range(0, len(tables))]
print(type(tables))
print(tables)
tables.remove('analytical_solutions_character')
database.clear_table('analytical_solutions_character', db_file)

tables.remove('analytical_solutions_weapon')
database.clear_table('analytical_solutions_weapon', db_file)
print(tables)
print()

# for table in tables:
#     database.print_table(table)
#     pass

# if not database.check_db(db_file):
#     with sqlite3.connect(db_file) as conn:
#         database.create_data_tables(conn)

analytical_object = AnalyticalRecursiveTest({})
print(len(analytical_object.hashtable))
analytical_object.calculate_and_write_all_solutions()
print(len(analytical_object.hashtable))

# "INSERT OR REPLACE INTO"
# analytical_object.update_all_analytical_db()

# temp = analytical_object.load_all_analytical_from_db()
# print(len(temp))
# analytical_object.hashtable.update(temp)

for i in range(0, analytical_object.max_lookup):
    if i % 10000 == 0:
        print(i, analytical_object.hashtable[i])
        pass
print(len(analytical_object.hashtable))

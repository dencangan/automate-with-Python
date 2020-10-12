import sqlite3
import os
import pandas as pd


def sql_db(df, db_dir, db_name, tbl_name=None, query=None):
    """
    Aggregated function to handle sqlite db creation/writing/querying to return a pandas DataFrame.
    """
    conn = sqlite3.connect(db_dir + "/" + db_name + '.sqlite', check_same_thread=False)

    if query is not None:
        print(f"Connecting to {db_name} database and querying...")
        return pd.read_sql(query, conn)

    else:
        if tbl_name is None:
            raise AssertionError(f"Must specify table name to create new database or write new table.")

        if os.path.exists(os.path.join(db_dir, db_name)):
            print(f"Database {db_name} already exists.")
            df.to_sql(tbl_name, conn)
            print(f"{tbl_name} table created in {db_name} database")

        else:
            print("Creating new database.")
            df.to_sql(tbl_name, conn)
            print(f"{db_name} database created in {db_dir} with table name {tbl_name}")

    conn.close()


def drop_table(c, tbl_name):
    cursor = c.cursor()
    q = f"DROP TABLE {tbl_name}"
    cursor.execute(q)
    c.close()


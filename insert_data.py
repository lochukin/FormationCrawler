import psycopg2
from config import config
from psycopg2.extras import execute_values


def insert(table: str, data: list):
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        columns = data[0].keys()
        query = "INSERT INTO {0} ({1}) VALUES %s".format(table, ','.join(columns))

        # convert projects values to sequence of seqences
        values = [[value for value in i.values()] for i in data]

        execute_values(cur, query, values)

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

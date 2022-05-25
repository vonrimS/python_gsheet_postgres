import psycopg2
import datetime as dt
import getpass


# Get db and user credentials, strip them to avoid some extra space symbols
hostname = (input('Enter hostname: ')).strip()
database = input('Enter database name: ').strip()
port_id = input('Enter port: ').strip()
username = input('Enter username: ').strip()
pwd = getpass.getpass('Enter password: ').strip()

conn = None
cur = None

# Get connection to DB with given credentials
def get_connection():

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)
        return conn
    except Exception as error:
        print(error)


# Create table in DB with known structure *new column named 'rub_cost' was added
def create_table_if_not_exist():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        create_script = ''' CREATE TABLE IF NOT EXISTS test (
                            id                 serial PRIMARY KEY,
                            order_number       int NOT NULL,
                            usd_cost           int NOT NULL,
                            rub_cost           int NOT NULL,
                            delivery_time      date)'''
        cur.execute(create_script)
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# Insert data into DB table
def insert_into_table(insert_values):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        insert_script = ''' INSERT INTO test
                            (id, order_number, usd_cost, rub_cost, delivery_time)
                            VALUES(%s,%s,%s,%s,%s)'''

        # Insert all data from tuple, piece by piece
        for value in insert_values:
            cur.execute(insert_script,value)
        conn.commit()
        print(f'{dt.datetime.now()}: ...data inserted')

    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# Delete data from DB table
def delete_from_table():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        delete_script = 'DELETE from test;'
        cur.execute(delete_script)
        conn.commit()
        print(f'{dt.datetime.now()}: ...db cleared')

    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

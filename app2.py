import psycopg2
from config import config

def create_table():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE notendur (
            userid INT NOT NULL PRIMARY KEY, 
            name VARCHAR(50) NOT NULL,
            username VARCHAR(32) NOT NULL,
            passw VARCHAR(32) NOT NULL
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
from sqlite3 import Connection, connect

def get_db_conn(db_name: str) -> Connection:
    connection = connect(db_name, check_same_thread=False)
    print("Connected to database...")
    return connection
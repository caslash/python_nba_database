from concurrent.futures import ThreadPoolExecutor

from api.proxies import get_proxies
from api.nba_api import (
    get_players
)

import db.connection as db_connection
import db.tables as db_tables


def main():
    connection = db_connection.get_db_conn("out/nba_db.db")
    proxies = get_proxies()

    db_tables.create_tables(connection)

    print("Starting database update...")

    get_players('players', proxies, connection)

    # tasks = [
    #     lambda: get_players('players', proxies, connection)
    # ]

    # with ThreadPoolExecutor() as executor:
    #     executor.map(lambda task: task(), tasks)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
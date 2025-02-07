from concurrent.futures import ThreadPoolExecutor

from api.proxies import get_proxies
from api.nba_api import (
    get_all_player_ids,
    get_players,
    get_player_accolades
)

import db.connection as db_connection
import db.tables as db_tables


def main():
    connection = db_connection.get_db_conn("out/nba_db.db")
    proxies = get_proxies()

    if len(proxies) == 0:
        print("No valid proxies could be found, try again.")
        return

    db_tables.create_tables(connection)

    print("Starting database update...")

    players = get_all_player_ids()

    get_players(players, 'player', proxies, connection),
    get_player_accolades(players, 'player_accolades', proxies, connection)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
from sqlite3 import Connection, Cursor

def create_tables(connection: Connection):
    if connection == None:
        print("No database connection found.")
        return

    cursor = connection.cursor()

    create_player_table(cursor)

    connection.commit()

def create_player_table(cursor: Cursor):
    player_query = '''
        CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        display_first_last TEXT,
        display_fi_last TEXT,
        birthdate TIMESTAMP,
        school TEXT,
        country TEXT,
        height TEXT,
        weight TEXT,
        season_exp INTEGER,
        jersey TEXT,
        position TEXT,
        team_history TEXT,
        is_active BOOLEAN,
        from_year INTEGER,
        to_year INTEGER,
        total_games_played INTEGER,
        draft_round TEXT,
        draft_number TEXT,
        draft_year TEXT);
    '''

    cursor.execute(player_query)
    print("Table 'player' created successfully...")
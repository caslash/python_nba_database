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
        CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        display_first_last VARCHAR,
        display_fi_last VARCHAR,
        birthdate TIMESTAMP,
        school VARCHAR,
        country VARCHAR,
        height VARCHAR,
        weight VARCHAR,
        season_exp INTEGER,
        jersey INTEGER,
        position VARCHAR,
        team_history VARCHAR,
        is_active BOOLEAN,
        from_year INTEGER,
        to_year INTEGER,
        total_games_played INTEGER,
        draft_round VARCHAR,
        draft_number VARCHAR,
        draft_year VARCHAR);
    '''

    cursor.execute(player_query)
    print("Table 'player' created successfully...")
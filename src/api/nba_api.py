from multiprocessing import Pool

from nba_api.stats.static import players
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.endpoints.playerprofilev2 import PlayerProfileV2

from numpy import random
from pandas import concat, Series, DataFrame
from sqlite3 import Connection
from functools import partial
from requests.exceptions import RequestException
from pandera.errors import SchemaErrors

from db.models import (
    PlayerSchema
)

def get_players_helper(player_id: str, proxies: Series):
    while True:
        try:
            selected_proxy = random.choice(proxies)
            df = CommonPlayerInfo(
                player_id, proxy=selected_proxy, timeout=3
            ).get_data_frames()[0]

            player_stats_df = PlayerProfileV2(
                per_mode36='PerGame', player_id=player_id, proxy=selected_proxy, timeout=3
            ).season_totals_regular_season.get_data_frame()
            filtered_df = player_stats_df[player_stats_df['TEAM_ID'] != 0]
            only_nba_df = filtered_df[filtered_df['LEAGUE_ID'] != 00]
            unique_team_ids = only_nba_df['TEAM_ID'].loc[only_nba_df['TEAM_ID'].shift() != only_nba_df['TEAM_ID']].astype(str).tolist()

            team_string = ','.join([str(id) for id in unique_team_ids])
            games_played = only_nba_df['GP'].sum()

            df['id'] = [int(player_id)]
            df['is_active'] = df['ROSTERSTATUS'].transform(lambda status: True if status == "Active" else False)
            df['team_history'] = [team_string]
            df['total_games_played'] = [games_played]

            df.columns = df.columns.to_series().apply(lambda x: x.lower())
            return df
        except RequestException:
            continue
        except ValueError:
            return None

def get_players(table_name: str, proxies: Series, connection: Connection):
    print("Getting players...")
    players_list = players.get_players()
    player_ids = DataFrame(players_list)['id'].astype("category")

    with Pool(250) as p:
        dfs = p.map(partial(get_players_helper, proxies=proxies), player_ids)
    dfs = [df for df in dfs if df is not None]
    dfs = concat(dfs, ignore_index=True).reset_index(drop=True)
    try:
        print("Validating player rows against schema...")
        dfs = PlayerSchema.validate(dfs, lazy=True, coerce=True, ignore_extra=True)
    except SchemaErrors as err:
        print("Schema validation failed for players")
        print(f"Schema errors: {err.failure_cases}")
        print(f"Invalid dataframe: {err.data}")
        return None
    print("Successfully retrieved all players.")
    dfs.to_sql(table_name, connection, if_exists="replace", index=False)
    return dfs

# {'id': 1627824, 'full_name': 'Guerschon Yabusele', 'first_name': 'Guerschon', 'last_name': 'Yabusele', 'is_active': True}
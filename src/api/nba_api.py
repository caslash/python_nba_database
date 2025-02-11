from multiprocessing import Pool
from multiprocessing.pool import IMapIterator
from pandera import Bool
from tqdm import tqdm

from nba_api.stats.static import players
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.endpoints.playerprofilev2 import PlayerProfileV2
from nba_api.stats.endpoints.playerawards import PlayerAwards

from numpy import random
from pandas import concat, Series, DataFrame
from sqlite3 import Connection
from functools import partial
from requests.exceptions import RequestException
from pandera.errors import SchemaErrors
from pandera.typing.common import (
    DataFrameBase
)

from db.models import (
    PlayerSchema,
    PlayerAccoladesSchema
)

def get_all_player_ids() -> Series:
    players_list = players.get_players()
    player_ids = DataFrame(players_list)['id'].astype('category')
    return player_ids

# ---HELPERS---
def get_players_helper(player_id: str, proxies: list[str]) -> DataFrame | None:
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

            df['id'] = [player_id]
            df['is_active'] = df['ROSTERSTATUS'].transform(lambda status: True if status == "Active" else False)
            df['team_history'] = [team_string]
            df['total_games_played'] = [games_played]

            df = df.drop(columns=['PERSON_ID', 'DISPLAY_LAST_COMMA_FIRST', 'PLAYER_SLUG', 'LAST_AFFILIATION', 'ROSTERSTATUS', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CODE', 'TEAM_CITY', 'PLAYERCODE', 'DLEAGUE_FLAG', 'NBA_FLAG', 'GAMES_PLAYED_FLAG', 'GAMES_PLAYED_CURRENT_SEASON_FLAG', 'GREATEST_75_FLAG'])

            df.columns = df.columns.to_series().apply(lambda x: x.lower())
            return df
        except RequestException:
            continue
        except ValueError:
            return None

def get_players(
    player_ids: Series,
    table_name: str,
    proxies: list[str],
    connection: Connection,
    save_to_db: bool = True,
    attempt: int = 1,
    max_attempts: int = 5
) -> list[DataFrame] | None:
    print('Adding players to database...')
    with Pool(250) as p:
        results_iterator: IMapIterator[DataFrame | None] = p.imap_unordered(
            partial(get_players_helper, proxies=proxies),
            player_ids,
            chunksize=10
        )
        dfs: list[DataFrame | None] = list(tqdm(
            results_iterator,
            total=len(player_ids),
            unit='player',
            desc='Loading players...',
            colour='red'
        ))
    successful_dfs = [df for df in dfs if df is not None]
    successful_ids = { df['id'].iloc[0] for df in successful_dfs if 'id' in df.columns }
    missing_ids = Series([pid for pid in player_ids if pid not in successful_ids])

    if (not missing_ids.empty) and (attempt < max_attempts):
        print(f'Attempt {attempt}: Retrying {len(missing_ids)} missing players...')
        missing_dfs: list[DataFrame] = get_players(missing_ids, table_name, proxies, connection, save_to_db=False, attempt=attempt+1, max_attempts=max_attempts) # type: ignore
        if missing_dfs is not None:
            successful_dfs.extend(missing_dfs)
    
    if not successful_dfs:
        print("No players were successfully retrieved.")
        return None

    if not save_to_db:
        return successful_dfs

    combined_df = concat(successful_dfs, ignore_index=True).reset_index(drop=True)
    try:
        print("Validating player rows against schema...")
        combined_df = PlayerSchema.validate(combined_df, lazy=True)
    except SchemaErrors as err:
        print("Schema validation failed for players")
        print(f"Schema errors: {err.failure_cases}")
        print(f"Invalid dataframe: {err.data}")
        return None
    print("Successfully retrieved all players. Saving to database...")
    combined_df.to_sql(table_name, connection, if_exists="append", index=False) # type: ignore
    print(f"Successfully saved {len(combined_df)} players to '{table_name}' table.") # type: ignore

def get_player_accolades_helper(player_id: str, proxies: list[str]):
    while True:
        try:
            selected_proxy = random.choice(proxies)

            df = DataFrame([player_id], columns=['player_id'])

            player_awards = PlayerAwards(player_id=player_id, proxy=selected_proxy, timeout=3).get_normalized_json()
            df['accolades_object'] = [str(player_awards)]

            df.columns = df.columns.to_series().apply(lambda x: x.lower())
            return df
        except RequestException:
            continue
        except ValueError:
            return None

def get_player_accolades(player_ids: Series, table_name: str, proxies: list[str], connection: Connection):
    print('Adding player accolades to database...')
    with Pool(250) as p:
        results_iterator = p.imap_unordered(partial(get_player_accolades_helper, proxies=proxies), player_ids)
        dfs = list(tqdm(results_iterator, total=len(player_ids), unit='player', desc="Loading player accolades...", colour='green'))
    dfs = [df for df in dfs if df is not None]
    dfs = concat(dfs, ignore_index=True).reset_index(drop=True)
    try:
        print("Validating player accolade rows against schema...")
        dfs = PlayerAccoladesSchema.validate(dfs, lazy=True)
    except SchemaErrors as err:
        print("Schema validation failed for player accolades")
        print(f"Schema errors: {err.failure_cases}")
        print(f"Invalid dataframe: {err.data}")
        return None
    print("Successfully retrieved all player accolades. Saving to database...")
    dfs.to_sql(table_name, connection, if_exists="append", index=False) # type: ignore
    print(f"Successfully saved {len(dfs)} players' accolades to '{table_name}' table.") # type: ignore
    return dfs
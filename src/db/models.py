import pandera as pa
from pandera import DataFrameModel
from pandera.typing import Series, Bool, String, Int, DateTime

class PlayerSchema(DataFrameModel):
    id: Series[String] = pa.Field(nullable=False)
    first_name: Series[String] = pa.Field(nullable=False)
    last_name: Series[String] = pa.Field(nullable=False)
    display_first_last: Series[String] = pa.Field(nullable=True)
    display_fi_last: Series[String] = pa.Field(nullable=True)
    birthdate: Series[DateTime] = pa.Field(nullable=True)
    school: Series[String] = pa.Field(nullable=True)
    country: Series[String] = pa.Field(nullable=True)
    height: Series[String] = pa.Field(nullable=True)
    weight: Series[String] = pa.Field(nullable=True)
    season_exp: Series[Int] = pa.Field(nullable=True)
    jersey: Series[String] = pa.Field(nullable=True)
    position: Series[String] = pa.Field(nullable=True)
    team_history: Series[String] = pa.Field(nullable=True)
    from_year: Series[Int] = pa.Field(nullable=True)
    to_year: Series[Int] = pa.Field(nullable=True)
    total_games_played: Series[Int] = pa.Field(nullable=True)
    draft_round: Series[String] = pa.Field(nullable=True)
    draft_number: Series[String] = pa.Field(nullable=True)
    draft_year: Series[String] = pa.Field(nullable=True)
    is_active: Series[Bool] = pa.Field(nullable=True)

    class Config:
        coerce = True
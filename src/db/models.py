import pandera as pa
from pandera import DataFrameModel
from pandera.typing import Series, Bool, String, Int, DateTime

class PlayerSchema(DataFrameModel):
    id: Series[String] = pa.Field(nullable=False)
    first_name: Series[String] = pa.Field(nullable=False)
    last_name: Series[String] = pa.Field(nullable=False)
    display_first_last: Series[String] = pa.Field(nullable=False)
    display_fi_last: Series[String] = pa.Field(nullable=False)
    birthdate: Series[DateTime] = pa.Field(nullable=True)
    school: Series[String] = pa.Field(nullable=True)
    country: Series[String] = pa.Field(nullable=False)
    height: Series[String] = pa.Field(nullable=True)
    weight: Series[String] = pa.Field(nullable=True)
    season_exp: Series[Int] = pa.Field(nullable=False)
    jersey: Series[Int] = pa.Field(nullable=True)
    position: Series[String] = pa.Field(nullable=False)
    team_history: Series[String] = pa.Field(nullable=False)
    from_year: Series[Int] = pa.Field(nullable=False)
    to_year: Series[Int] = pa.Field(nullable=False)
    total_games_played: Series[Int] = pa.Field(nullable=False)
    draft_round: Series[String] = pa.Field(nullable=True)
    draft_number: Series[String] = pa.Field(nullable=True)
    draft_year: Series[String] = pa.Field(nullable=True)
    isActive: Series[Bool] = pa.Field(nullable=False)

    class Config:
        coerce = True
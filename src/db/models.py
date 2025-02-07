import pandera as pa
from pandera import DataFrameModel
from pandera.typing import Series, Bool, String, Int, DateTime

class PlayerSchema(DataFrameModel):
    id: Series[String] = pa.Field(nullable=False, coerce=True)
    first_name: Series[String] = pa.Field(nullable=False, coerce=True)
    last_name: Series[String] = pa.Field(nullable=False, coerce=True)
    display_first_last: Series[String] = pa.Field(nullable=False, coerce=True)
    display_fi_last: Series[String] = pa.Field(nullable=False, coerce=True)
    birthdate: Series[DateTime] = pa.Field(nullable=True, coerce=True)
    school: Series[String] = pa.Field(nullable=True, coerce=True)
    country: Series[String] = pa.Field(nullable=False, coerce=True)
    height: Series[String] = pa.Field(nullable=True, coerce=True)
    weight: Series[String] = pa.Field(nullable=True, coerce=True)
    season_exp: Series[Int] = pa.Field(nullable=False, coerce=True)
    jersey: Series[Int] = pa.Field(nullable=True, coerce=True)
    position: Series[String] = pa.Field(nullable=False, coerce=True)
    team_history: Series[String] = pa.Field(nullable=False, coerce=True)
    from_year: Series[Int] = pa.Field(nullable=False, coerce=True)
    to_year: Series[Int] = pa.Field(nullable=False, coerce=True)
    total_games_played: Series[Int] = pa.Field(nullable=False, coerce=True)
    draft_round: Series[String] = pa.Field(nullable=True, coerce=True)
    draft_number: Series[String] = pa.Field(nullable=True, coerce=True)
    draft_year: Series[String] = pa.Field(nullable=True, coerce=True)
    is_active: Series[Bool] = pa.Field(nullable=False, coerce=True)

    class Config:
        coerce = True
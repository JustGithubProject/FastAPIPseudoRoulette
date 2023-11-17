from datetime import datetime
from pydantic import BaseModel


class RouletteCellCreate(BaseModel):
    weight: int


class RouletteSpinCreate(BaseModel):
    round_id: int
    user_id: int
    selected_cell: int


class RouletteRoundCreate(BaseModel):
    jackpot_cell_id: int


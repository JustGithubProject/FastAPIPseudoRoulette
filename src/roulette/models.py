import sqlalchemy as sql
from sqlalchemy.orm import relationship
from src.database import Base

import datetime


class RouletteRound(Base):
    __tablename__ = "roulette_rounds"

    round_id = sql.Column(sql.Integer, primary_key=True)
    timestamp = sql.Column(sql.DateTime, default=datetime.datetime.utcnow)
    jackpot_cell_id = sql.Column(sql.Integer, sql.ForeignKey("roulette_cells.cell_id"))

    jackpot_cell = relationship("RouletteCell")


class RouletteSpin(Base):
    __tablename__ = "roulette_spins"
    spin_id = sql.Column(sql.Integer, primary_key=True)
    round_id = sql.Column(sql.Integer, sql.ForeignKey("roulette_rounds.round_id"))
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    selected_cell = sql.Column(sql.Integer)

    round = relationship("RouletteRound")
    user = relationship("User")


class RouletteCell(Base):
    __tablename__ = "roulette_cells"

    cell_id = sql.Column(sql.Integer, primary_key=True)
    weight = sql.Column(sql.Float)




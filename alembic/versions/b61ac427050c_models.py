"""models

Revision ID: b61ac427050c
Revises: 52a0aa496374
Create Date: 2023-11-09 20:58:58.512577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
import datetime

# revision identifiers, used by Alembic.
revision: str = 'b61ac427050c'
down_revision: Union[str, None] = '52a0aa496374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roulette_cells",
        sa.Column("cell_id", sa.Integer, primary_key=True),
        sa.Column("weight", sa.Float),
    )
    op.create_table(
        "roulette_rounds",
        sa.Column("round_id", sa.Integer, primary_key=True),
        sa.Column("timestamp", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("jackpot_cell_id", sa.Integer, sa.ForeignKey("roulette_cells.cell_id"))
    )

    op.create_table(
        "roulette_spins",
        sa.Column("spin_id", sa.Integer, primary_key=True),
        sa.Column("round_id", sa.Integer, sa.ForeignKey("roulette_rounds.round_id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("selected_cell", sa.Integer),
    )



def downgrade() -> None:
    op.drop_table("roulette_cells")
    op.drop_table("roulette_spins")
    op.drop_table("roulette_rounds")

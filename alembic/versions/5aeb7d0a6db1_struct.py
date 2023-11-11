from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5aeb7d0a6db1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False)
    )
    op.create_table(
        'roulette_cells',
        sa.Column('cell_id', sa.Integer, primary_key=True),
        sa.Column('weight', sa.Float)
    )

    op.create_table(
        'roulette_rounds',
        sa.Column('round_id', sa.Integer, primary_key=True),
        sa.Column('timestamp', sa.DateTime, default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('jackpot_cell_id', sa.Integer, sa.ForeignKey("roulette_cells.cell_id"))
    )

    op.create_table(
        'roulette_spins',
        sa.Column('spin_id', sa.Integer, primary_key=True),
        sa.Column('round_id', sa.Integer, sa.ForeignKey("roulette_rounds.round_id")),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('selected_cell', sa.Integer)
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('roulette_rounds')
    op.drop_table('roulette_spins')
    op.drop_table('roulette_cells')

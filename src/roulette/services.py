from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.roulette.models import RouletteSpin
from src.roulette.schemas import RouletteCellCreate
from src.roulette.schemas import RouletteSpinCreate
from src.roulette.models import RouletteCell
from src.roulette.models import RouletteRound
from src.roulette.schemas import RouletteRoundCreate


class RouletteCellRepository:
    """Repository to work with RouletteCell model"""
    def __init__(self, session):
        self.session = session

    async def create_roulette_cells_(self, roulette_cells: RouletteCellCreate):
        roulette_cells_obj = RouletteCell(weight=roulette_cells.weight)
        self.session.add(roulette_cells_obj)
        await self.session.commit()
        await self.session.refresh(roulette_cells_obj)
        return roulette_cells_obj

    async def get_list_roulette_cells_(self):
        stmt = select(RouletteCell)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items

    async def get_roulette_cell_by_id(self, cell_id: int):
        stmt = select(RouletteCell).where(RouletteCell.cell_id == cell_id)
        result = await self.session.execute(stmt)
        roulette_cell = result.scalar_one_or_none()
        return roulette_cell


class RouletteSpinRepository:
    """Repository to work with RouletteSpin"""
    def __init__(self, session):
        self.session = session

    async def create_roulette_spin_(self, roulette_spin: RouletteSpinCreate):
        roulette_spin_obj = RouletteSpin(
            round_id=roulette_spin.round_id,
            user_id=roulette_spin.user_id,
            selected_cell=roulette_spin.selected_cell
        )
        self.session.add(roulette_spin_obj)
        await self.session.commit()
        await self.session.refresh(roulette_spin_obj)
        return roulette_spin_obj

    async def get_list_roulette_spin_(self):
        stmt = select(RouletteSpin)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items


class RouletteRoundRepository:
    """Repository to work with RouletteRound"""
    def __init__(self, session):
        self.session = session

    async def create_roulette_round_(self, roulette_round: RouletteRoundCreate):
        roulette_round_obj = RouletteRound(
            jackpot_cell_id=roulette_round.jackpot_cell_id
        )
        self.session.add(roulette_round_obj)
        await self.session.commit()
        await self.session.refresh(roulette_round_obj)
        return roulette_round_obj

    async def get_roulette_round_by_round_id(self, r_id: int):
        stmt = select(RouletteRound).options(
            selectinload(RouletteRound.jackpot_cell)
        ).where(RouletteRound.round_id == r_id)
        result = await self.session.execute(stmt)
        item = result.scalars().first()
        return item

    async def get_list_roulette_round_(self):
        stmt = select(RouletteRound)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items


from sqlalchemy import select

from src.roulette.schemas import RouletteCellCreate
from src.roulette.models import RouletteCell


class RouletteCellRepository:
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

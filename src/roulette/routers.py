import random

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.roulette.schemas import RouletteRoundCreate
from src.roulette.services import RouletteRoundRepository
from src.roulette.schemas import RouletteCellCreate
from src.roulette.schemas import RouletteSpinCreate
from src.roulette.services import RouletteCellRepository
from src.database import get_async_session
from src.roulette.services import RouletteSpinRepository

router_roulette = APIRouter(tags=["roulette"])


async def get_roulette_cells_repository(session: AsyncSession = Depends(get_async_session)):
    """The function that gives session to RouletteCellRepository"""
    return RouletteCellRepository(session)


async def get_roulette_round_repository(session: AsyncSession = Depends(get_async_session)):
    """The function that gives session to RouletteRoundRepository"""
    return RouletteRoundRepository(session)


async def get_roulette_spin_repository(session: AsyncSession = Depends(get_async_session)):
    """The function that gives session to RouletteSpinRepository"""
    return RouletteSpinRepository(session)


@router_roulette.post("/api/create/roulette_cells")
async def create_roulette_cells(

        roulette_cells: RouletteCellCreate,
        roulette_cells_repository: RouletteCellRepository = Depends(get_roulette_cells_repository)
    ):
    """The function to create cell with a certain weight"""
    return await roulette_cells_repository.create_roulette_cells_(roulette_cells=roulette_cells)


@router_roulette.get("/api/list/roulette_cells")
async def get_list_roulette_cells(
        roulette_cells_repository: RouletteCellRepository = Depends(get_roulette_cells_repository)
    ):
    """The function to get list of cells"""
    return await roulette_cells_repository.get_list_roulette_cells_()


@router_roulette.post("/api/create/roulette_round")
async def create_roulette_round(
        roulette_round: RouletteRoundCreate,
        roulette_round_repository: RouletteRoundRepository = Depends(get_roulette_round_repository)
    ):
    """The function to create roulette round"""
    return await roulette_round_repository.create_roulette_round_(roulette_round=roulette_round)


@router_roulette.get("/api/list/roulette_round")
async def get_list_roulette_round(
        roulette_round_repository: RouletteRoundRepository = Depends(get_roulette_round_repository)
    ):
    return await roulette_round_repository.get_list_roulette_round_()


@router_roulette.get("/api/create/spin")
async def spin_roulette(
        roulette_cells_repository: RouletteCellRepository = Depends(get_roulette_cells_repository)
    ):
    list_cells_temp = await roulette_cells_repository.get_list_roulette_cells_()
    list_cells = [i.cell_id for i in list_cells_temp]

    list_weight = [i.weight for i in list_cells_temp]
    roulette_result = random.choices(list_cells, list_weight)[0]
    return roulette_result




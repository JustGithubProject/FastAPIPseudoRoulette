import random

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.roulette.models import RouletteRound
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


@router_roulette.post("/api/create/spin")
async def spin_roulette(
        roulette_spin: RouletteSpinCreate,
        roulette_round_repository: RouletteRoundRepository = Depends(get_roulette_round_repository),
        roulette_cells_repository: RouletteCellRepository = Depends(get_roulette_cells_repository),
        roulette_spin_repository: RouletteSpinRepository = Depends(get_roulette_spin_repository)
    ):
    if roulette_spin.round_id == 1:
        list_cells_temp = await roulette_cells_repository.get_list_roulette_cells_()
        list_cells = [i.cell_id for i in list_cells_temp]

        list_weight = [i.weight for i in list_cells_temp]
        roulette_result = random.choices(list_cells, list_weight)[0]
    else:
        list_cells_temp = await roulette_cells_repository.get_list_roulette_cells_()
        except_list_cells = []
        except_list_weight = []
        for i in range(1, int(roulette_spin.round_id)):
            roulette_r = await roulette_round_repository.get_roulette_round_by_round_id(i)
            except_list_cells.append(roulette_r.jackpot_cell_id)
            except_list_weight.append(roulette_r.weight)

        list_cells = [i.cell_id for i in list_cells_temp if i.cell_id not in except_list_cells]
        list_weight = [i.weight for i in list_cells_temp if i.weight not in except_list_weight]
        roulette_result = random.choices(list_cells, list_weight)[0]
    await roulette_spin_repository.create_roulette_spin_(roulette_spin)
    roulette_r = await roulette_round_repository.get_roulette_round_by_round_id(roulette_spin.round_id)
    if roulette_r:
        # Load the object using a query, make modifications, and commit changes
        roulette_round_query = select(RouletteRound).where(RouletteRound.round_id == roulette_spin.round_id)
        existing_roulette_round = await roulette_round_repository.session.execute(roulette_round_query)
        existing_roulette_round = existing_roulette_round.scalar_one()
        existing_roulette_round.jackpot_cell_id = roulette_result
        await roulette_round_repository.session.commit()
    return roulette_result




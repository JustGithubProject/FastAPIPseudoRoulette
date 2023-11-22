import random
import datetime

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
    """route to create cell with a certain weight"""
    return await roulette_cells_repository.create_roulette_cells_(roulette_cells=roulette_cells)


@router_roulette.get("/api/list/roulette_cells")
async def get_list_roulette_cells(
        roulette_cells_repository: RouletteCellRepository = Depends(get_roulette_cells_repository)
):
    """route to get list of cells"""
    return await roulette_cells_repository.get_list_roulette_cells_()


@router_roulette.post("/api/create/roulette_round")
async def create_roulette_round(
        roulette_round: RouletteRoundCreate,
        roulette_round_repository: RouletteRoundRepository = Depends(get_roulette_round_repository)
):
    """route to create roulette round"""
    return await roulette_round_repository.create_roulette_round_(roulette_round=roulette_round)


@router_roulette.get("/api/list/roulette_round")
async def get_list_roulette_round(
        roulette_round_repository: RouletteRoundRepository = Depends(get_roulette_round_repository)
):
    """route to get list of roulette_rounds"""
    return await roulette_round_repository.get_list_roulette_round_()


@router_roulette.post("/api/create/spin")
async def spin_roulette(
        roulette_spin: RouletteSpinCreate,
        roulette_round_repository: RouletteRoundRepository = Depends(get_roulette_round_repository),
        roulette_cells_repository: RouletteCellRepository = Depends(get_roulette_cells_repository),
        roulette_spin_repository: RouletteSpinRepository = Depends(get_roulette_spin_repository),
        session: AsyncSession = Depends(get_async_session)
):
    """The route Spin roulette"""
    try:
        # If round_id = 1 it means that we can use all cells
        if roulette_spin.round_id == 1:
            list_cells_temp = await roulette_cells_repository.get_list_roulette_cells_()
            # Generate random value using cells and weights
            roulette_results = random.choices(list_cells_temp, weights=[cell.weight for cell in list_cells_temp], k=1)
            roulette_result = roulette_results[0].cell_id

        # if round_id != 1 it means that we can use all cells except for those cells that have already fallen out
        else:
            list_cells_temp = await roulette_cells_repository.get_list_roulette_cells_()
            except_list_cells = set()
            except_list_weight = []

            # Generate the list in order to except the cells that have already fallen out
            for i in range(1, int(roulette_spin.round_id)):
                roulette_r = await roulette_round_repository.get_roulette_round_by_round_id(i)
                except_list_cells.add(roulette_r.jackpot_cell_id)
                roulette_cell = await roulette_cells_repository.get_roulette_cell_by_id(roulette_r.jackpot_cell_id)
                except_list_weight.append(roulette_cell.weight)

            # Get cells and weights that might fall
            filtered_cells = [cell for cell in list_cells_temp if cell.cell_id not in except_list_cells]
            filtered_weights = [cell.weight for cell in list_cells_temp if cell.cell_id not in except_list_cells]

            # Generate random value using cells and weights
            roulette_results = random.choices(filtered_cells, weights=filtered_weights, k=1)
            roulette_result = roulette_results[0].cell_id

        # Create spin
        await roulette_spin_repository.create_roulette_spin_(roulette_spin)

        # Get roulette_round by id
        roulette_r = await roulette_round_repository.get_roulette_round_by_round_id(roulette_spin.round_id)
        # if it exists.We assign cell that fell in roulette_spin
        if roulette_r:
            roulette_r.jackpot_cell_id = roulette_result
            roulette_r.timestamp = datetime.datetime.utcnow()
            await session.commit()
        else:
            print("Could not find roulette_r")
    except Exception as e:
        # Log the exception or print for debugging
        print(f"Error: {e}")
        return {"error": str(e)}

    return {"roulette_result": roulette_result}


@router_roulette.get("/api/list/spins")
async def get_spins(roulette_spin_repository: RouletteSpinRepository = Depends(get_roulette_spin_repository)):
    """Route to get list of spins"""
    return await roulette_spin_repository.get_list_roulette_spin_()




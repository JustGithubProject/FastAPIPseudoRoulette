from fastapi import FastAPI

from src.users.routers import router_user
from src.roulette.routers import router_roulette


app = FastAPI()


app.include_router(router_user)
app.include_router(router_roulette)


@app.get("/")
async def home():
    return {"status_code": 200, "request_method": "GET"}



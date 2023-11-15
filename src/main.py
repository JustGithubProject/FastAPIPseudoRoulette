from fastapi import FastAPI

from src.users.routers import router_user

app = FastAPI()


app.include_router(router_user)


@app.get("/")
async def home():
    return {"status_code": 200, "request_method": "GET"}



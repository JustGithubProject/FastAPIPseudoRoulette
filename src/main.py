from fastapi import FastAPI

from src.users.routers import router

app = FastAPI()


app.include_router(router)


@app.get("/")
async def home():
    return {"status_code": 200, "request_method": "GET"}



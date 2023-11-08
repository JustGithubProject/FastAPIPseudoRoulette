from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
    return {"status_code": 200, "request_method": "GET"}



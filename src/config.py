import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    DB_NAME = os.environ.get("DB_NAME")





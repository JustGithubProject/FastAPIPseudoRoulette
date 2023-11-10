import os

from dotenv import load_dotenv

env_path = r"D:/Users/Kropi/PycharmProjects/Instreadolx/.env"

load_dotenv(dotenv_path=env_path)

USERNAME = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DB_NAME = os.environ.get("DB_NAME")


print(f"USERNAME: {USERNAME}")
print(f"PASSWORD: {PASSWORD}")
print(f"HOST: {HOST}")
print(f"PORT: {PORT}")
print(f"DB_NAME: {DB_NAME}")

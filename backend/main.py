import os

import psycopg
from fastapi import FastAPI

app = FastAPI()


@app.get("/status")
def status():
    return {"message": "Backend działa!"}


@app.get("/db-status")
def db_status():
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

    return {"database": "connected", "result": result[0]}
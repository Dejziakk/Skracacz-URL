import os

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, HttpUrl
import random
import string

app = FastAPI(root_path="/api")

def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

@app.get("/status")
def status():
    return {"message": "Backend działa!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-status")
def db_status():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

    return {"database": "connected", "result": result[0]}

@app.get("/link/{link_id}")
def get_link(link_id: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT code, url FROM links WHERE code = %s",
                (link_id,)
            )
            row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"code": row[0], "link": row[1]}

@app.get("/link")
def get_links():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    links.code,
                    links.url,
                    COUNT(visits.id)
                FROM links
                LEFT JOIN visits ON links.id = visits.link_id
                GROUP BY links.id, links.code, links.url
                ORDER BY links.id
            """)
            rows = cursor.fetchall()

    return [
        {
            "code": row[0],
            "link": row[1],
            "visits": row[2]
        }
        for row in rows
    ]


class NewLink(BaseModel):
    link: HttpUrl
    code: str | None = Field(default=None, min_length=2, max_length=20)

@app.post("/link")
def post_link(link: NewLink):
    code = link.code

    if code is None:
        code = "".join(random.choices(string.ascii_letters, k=6))

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM links WHERE code = %s",
                (code,)
            )

            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Link already exists"
                )

            cursor.execute(
                "INSERT INTO links (code, url) VALUES (%s, %s)",
                (code, str(link.link))
            )

    return {"code": code, "link": str(link.link)}

@app.delete("/link/{link_id}")
def delete_link(link_id: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM links WHERE code = %s RETURNING code, url",
                (link_id,)
            )
            row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"code": row[0], "link": row[1]}

@app.get("/r/{code}")
def redirect_link(code: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, url FROM links WHERE code = %s",
                (code,)
            )
            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="Link not found"
                )

            link_id = row[0]
            original_url = row[1]

            cursor.execute(
                "INSERT INTO visits (link_id) VALUES (%s)",
                (link_id,)
            )

    return RedirectResponse(
        url=original_url,
        status_code=307
    )
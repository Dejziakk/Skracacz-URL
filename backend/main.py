import os

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import random
import string 

app = FastAPI()
links = {}

@app.get("/status")
def status():
    return {"message": "Backend działa!"}

@app.get("/health")
def health():
    return {"status": "ok"}

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

@app.get("/link/{link_id}")
def get_link(link_id):
    if link_id not in links:
        raise HTTPException(status_code=404, detail="Link not found")
    link = links[link_id]
    return link

@app.get("/link")
def get_links():
    return list(links.values())
    
class NewLink(BaseModel):
    link: str
    code: str | None = Field(default=None, min_length=2, max_length=20)
    
@app.post("/link")
def post_link(link: NewLink):
    code = link.code
    if code is None:
        arr = random.choices(string.ascii_letters, k=6)
        code = "".join(arr)
        
    if code in links:
        raise HTTPException(status_code=400, detail="Link already exists")
    
    links[code] = {"link": link.link, "code": code}
    return links[code]

@app.delete("/link/{link_id}")
def delete_link(link_id):
    if link_id not in links:
        raise HTTPException(status_code=404, detail="Link not found")
    return links.pop(link_id)
    
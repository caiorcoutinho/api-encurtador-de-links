from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import src.database as db

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def v1():
    return JSONResponse(content={"message": "API working", "status_code": 200}, status_code=200)

class Urls(BaseModel):
    original_url: str
    shorten_url: str

@app.post("/shorten", )
def short_url(urls: Urls):
    shorten_url = db.create(original_url=urls.original_url, shorten_url=urls.shorten_url)
    if not shorten_url:
        raise HTTPException(status_code=409)
    return JSONResponse(content={"message": "Shortened url created", "status_code": 200}, status_code=200)

@app.get("/{shorten_url}")
def get_original_url(shorten_url: str):
    data = db.find_original_url(shorten_url)
    if not data:
        raise HTTPException(status_code=404)
    return RedirectResponse(data['original_url'])
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from pydantic.types import StringConstraints
from typing import Annotated
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

index = ""
with open('index.html', "r") as html:
    index = html.read()

@app.get("/", include_in_schema=False)
def v1():
    return HTMLResponse(index)

class Urls(BaseModel):
    original_url: HttpUrl
    shorten_url: Annotated[
        str,
        StringConstraints(
            max_length=10,
            pattern=r"^[a-zA-Z0-9_-]+$",
        )
    ]

@app.post("/shorten", include_in_schema=False)
def short_url(urls: Urls):
    try:
        original_url = str(urls.original_url)
        shorten_url = urls.shorten_url
        success = db.create(original_url=original_url, shorten_url=shorten_url)
        if not success:
            raise HTTPException(status_code=409)
        return JSONResponse(content={"message": "Shortened url created", "status_code": 200}, status_code=200)
    except Exception as e:
        print(str(e), e)
        raise HTTPException(status_code=500)

@app.get("/{shorten_url}", include_in_schema=False)
def get_original_url(shorten_url: str):
    data = db.find_original_url(shorten_url)
    if not data:
        raise HTTPException(status_code=404)
    return RedirectResponse(data['original_url'], status_code=308)
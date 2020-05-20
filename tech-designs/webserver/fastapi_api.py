#!/usr/bin/env python3
from ipaddress import IPv4Address
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, SecretStr

app = FastAPI()


@app.get("/health")
def health():
    return PlainTextResponse("OK")


class Validated(BaseModel):
    addr: IPv4Address
    login: str
    password: Optional[SecretStr]


@app.post("/validate")
def validate_json(body: Validated):
    return PlainTextResponse("OK")


app.mount("/static", StaticFiles(directory="./static"), name="static")


if __name__ == "__main__":
    uvicorn.run("fastapi_uvicorn:app", workers=1, port=5000)

#!/usr/bin/env python3
import logging

from aiohttp import web
from aiohttp_apispec import (
    docs,
    json_schema,
    validation_middleware,
    setup_aiohttp_apispec,
)
from marshmallow import Schema, fields

logging.basicConfig(level=logging.DEBUG)

app = web.Application()
routes = web.RouteTableDef()


@routes.get("/health")
async def health(request):
    return web.Response(body="OK")


class Validated(Schema):
    addr = fields.String(required=True)
    login = fields.String(required=True)
    password = fields.String()


@routes.post("/validate")
@docs(
    tags=["validate"],
    responses={
        200: {"description": "OK"},
        422: {"description": "Validation error"}
    }
)
@json_schema(Validated)
async def validate_json(request):
    return web.Response(body="OK")


routes.static("/static", "./static")

app.add_routes(routes)
app.middlewares.append(validation_middleware)

setup_aiohttp_apispec(app)

if __name__ == "__main__":
    web.run_app(app, port=5000, host="127.0.0.1")

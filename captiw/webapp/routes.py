from http import HTTPStatus

from aiohttp.web import Request, Response, RouteTableDef

routes = RouteTableDef()


@routes.get("/health")
async def health(request: Request) -> Response:
    return Response(status=HTTPStatus.OK)

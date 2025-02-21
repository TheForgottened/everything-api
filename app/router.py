from typing import Annotated

from fastapi import APIRouter, Request, Depends
from starlette.responses import JSONResponse

from app.config.constants import HTTP_METHODS_LIST
from app.service import Service
from app.types import JSONable

router = APIRouter()


@router.api_route(
    path="/{uri:path}",
    methods=HTTP_METHODS_LIST,
    response_model=JSONable,
)
def do(service: Annotated[Service, Depends()], request: Request) -> JSONResponse:
    method: str = request.scope["method"]
    path: str = request.scope["path"]
    headers: dict[str, str] = dict(request.headers)
    query_params: list[tuple[str, str]] = request.query_params.multi_items()
    body = request.body()

    response = service.generate_response(
        method=method, path=path, headers=headers, query_params=query_params, body=body
    )

    return JSONResponse(status_code=response.status_code, headers=response.headers, content=response.body)

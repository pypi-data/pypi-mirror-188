import contextlib
import json
import os
from datetime import datetime
from typing import Callable, Union
from uuid import uuid4

from fastapi import (
    APIRouter,
    FastAPI,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.routing import APIRoute

from teleskope import __version__
from teleskope.log import log
from teleskope.types import (
    HealthResponse,
    JsonResponseLoggerMessage,
    RequestLoggerMessage,
    ResponseLoggerMessage,
)
from teleskope.ws import wcm

os.environ["TZ"] = "UTC"

app = FastAPI()


class _APIRoute(APIRoute):
    """_APIRoute.
    _APIRoute is a custom APIRoute class that adds a background task to the
    response to log request and response data.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def _log(
            req: RequestLoggerMessage,
            res: Union[JsonResponseLoggerMessage, ResponseLoggerMessage],
        ) -> None:
            id = {"id": str(uuid4()).replace("-", "")}
            log.info({**json.loads(req.json()), **id})
            log.info({**json.loads(res.json()), **id})

        async def custom_route_handler(request: Request) -> Response:
            req = RequestLoggerMessage(**request.__dict__)
            response = await original_route_handler(request)
            # if the response headers contain a content-type of application/json
            # then log the response body
            res: Union[JsonResponseLoggerMessage, ResponseLoggerMessage]
            if response.headers.get("content-type") == "application/json":
                res = JsonResponseLoggerMessage(**response.__dict__)
            else:
                res = ResponseLoggerMessage(**response.__dict__)
            await _log(req=req, res=res)
            return response

        return custom_route_handler


ws_router = APIRouter(route_class=_APIRoute, tags=["ws"])
health_router = APIRouter(route_class=_APIRoute, tags=["health"])


@health_router.get("/healthcheck", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Get the health of the server.

    Returns:
        HealthResponse: The health of the server.
    """
    log.info("Healthcheck!")
    return HealthResponse(message="⛵️", version=__version__, time=datetime.utcnow())


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Websocket endpoint.

    Args:
        websocket (WebSocket): The websocket connection.
    """
    await wcm.connect(websocket)
    with contextlib.suppress(WebSocketDisconnect):
        while True:
            data = await websocket.receive_bytes()
            decoded_data = data.decode("utf-8")
            await wcm.send_to_socket(
                message=f"{decoded_data} written by {websocket}",
                websocket=websocket,
            )
            await wcm.broadcast(f"{decoded_data} written by {websocket}")
    wcm.disconnect(websocket)
    await wcm.broadcast("disconnected from websocket")


app.include_router(ws_router)
app.include_router(health_router)

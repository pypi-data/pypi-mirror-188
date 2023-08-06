import asyncio
from typing import Optional
from uuid import uuid4

import websockets
from pydantic import UUID4

from teleskope.config import Config, _config
from teleskope.types import Message


class Client:
    def __init__(
        self,
        id: Optional[UUID4] = None,
        config: Optional[Config] = None,
    ) -> None:
        self.id = id or uuid4()
        self.config = config or _config
        self.ws = None
        self._set_ws()

    def _set_ws(self) -> None:
        asyncio.get_event_loop().run_until_complete(self._ws())

    async def _ws(self) -> None:
        ws = await websockets.connect(self.config.ws_url)  # type: ignore
        self.ws = ws

    def _send(self, data: bytes) -> None:
        self.ws.send(data)  # type: ignore

    def send(self, message: Message) -> None:
        self._send(data=message.json().encode("utf-8"))


teleskope_client = Client()

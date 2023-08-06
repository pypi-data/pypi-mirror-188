from datetime import datetime
from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel, Json, StrictInt, StrictStr


class HealthResponse(BaseModel):
    message: StrictStr
    version: StrictStr
    time: datetime


class Scope(BaseModel):
    type: StrictStr
    asgi: Optional[Dict]
    http_version: StrictStr
    method: StrictStr
    scheme: StrictStr
    root_path: Optional[StrictStr]
    path: StrictStr
    raw_path: Optional[str]
    headers: List
    query_string: bytes


class RequestLoggerMessage(BaseModel):
    scope: Scope
    _stream_consumed: bool
    _is_disconnected: bool


class ResponseLoggerMessage(BaseModel):
    status_code: StrictInt
    raw_headers: List


class JsonResponseLoggerMessage(BaseModel):
    body: Json


class Message(BaseModel):
    ns_id: UUID4
    df_id: UUID4
    data: StrictStr

    class Config:
        schema_extra = {
            "example": {
                "ns_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                "df_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
                "data": {"message": "Hello world!"},
            }
        }

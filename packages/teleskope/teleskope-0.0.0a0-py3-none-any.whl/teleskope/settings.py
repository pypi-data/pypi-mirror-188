import os
import sys

from pydantic import BaseSettings, Field


class _Env(BaseSettings):
    #
    #   Required
    #
    API_SECRET_KEY: str = Field(
        ...,
        env="API_SECRET_KEY",
        description="The API secret key.",
    )
    #
    #   Optional
    #
    LOG_LEVEL: str = Field(
        "INFO",
        env="LOG_LEVEL",
        description="Log level.",
    )
    WS_URL: str = Field(
        "ws://localhost:8000/ws",
        env="WS_URL",
        description="The websocket URL.",
    )

    class Config:
        env_file = ".env.local"
        env_encoding = "utf-8"


env = _Env()
if "pytest" in "".join(sys.argv):
    env = _Env(_env_file=".env.test")

# if the ENV_FILE environment variable is set, use it
# this is useful for running alembic migrations against remote databases
if os.getenv("ENV_FILE") is not None:
    env = _Env(_env_file=os.environ["ENV_FILE"])  # pragma: no cover

import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from pydantic import UUID4, BaseModel, Field, StrictStr


class Config(BaseModel):
    config_path: StrictStr = Field(
        default=f"{os.environ['HOME']}/.teleskope/config.json",
        description="The path to the config file",
    )
    namespace_id: Optional[UUID4] = Field(
        description="The namespace ID",
    )
    server_url: StrictStr = Field(
        default="http://localhost:8000",
        description="The teleskope API URL",
    )
    ws_url: StrictStr = Field(
        default="ws://localhost:8000/ws",
        description="The teleskope WebSocket URL",
    )

    def init(self) -> None:
        if Path(self.config_path).exists():
            self.load()
        else:
            self.save()

    def load(self) -> Dict:
        return self._load_config()

    def save(self) -> None:
        self._save_config()

    def _load_config(self) -> Dict:
        with open(self.config_path, "r") as f:
            return json.load(f)

    def _save_config(self) -> None:
        data = json.loads(self.json())
        # if the config file dir doesn't exist, create it
        Path(os.path.dirname(self.config_path)).mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(data, f)


_config = Config()

if "pytest" in "".join(sys.argv):  # pragma: no cover
    config_path = f"{os.environ['HOME']}/.teleskope/config.json.test"
    _config = Config(config_path=config_path)

_config.init()

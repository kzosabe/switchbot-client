from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from switchbot_client.devices import SwitchBotCommandResult

if TYPE_CHECKING:
    from switchbot_client import SwitchBotClient


@dataclass()
class SwitchBotScene:
    client: SwitchBotClient
    scene_id: str
    scene_name: str

    def __post_init__(self):
        if self.client is None:
            raise TypeError
        if self.scene_id is None:
            raise TypeError

    def execute(self) -> SwitchBotCommandResult:
        response = self.client.api_client.scenes_execute(self.scene_id)
        return SwitchBotCommandResult(response.status_code, response.message, response.body)

    def __repr__(self):
        data = {
            "scene_id": self.scene_id,
            "scene_name": self.scene_name,
        }
        return self.__class__.__qualname__ + f"({data})"

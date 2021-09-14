from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from switchbot_client.api import SwitchBotAPIClient, SwitchBotAPIResponse


class SwitchBotDevice:
    def __init__(self, client: SwitchBotAPIClient, device_id: str, device_type: str):
        if client is None:
            raise TypeError
        self.client = client
        if device_id is None:
            raise TypeError
        self.device_id = device_id
        self.device_type = device_type

    def status(self) -> SwitchBotAPIResponse:
        return self.client.devices_status(self.device_id)

    def control(
        self, command: str, parameter: str = None, command_type: str = None
    ) -> SwitchBotAPIResponse:
        return self.client.devices_commands(self.device_id, command, parameter, command_type)

    def __repr__(self):
        return f"<{self.device_type},{self.device_id}>"

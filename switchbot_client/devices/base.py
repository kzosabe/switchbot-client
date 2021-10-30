from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from switchbot_client.devices.status import DeviceStatus

if TYPE_CHECKING:
    from switchbot_client.api import SwitchBotAPIClient


@dataclass()
class SwitchBotDevice(ABC):
    client: SwitchBotAPIClient
    device_id: str
    device_type: str
    device_name: str
    hub_device_id: Optional[str]
    is_virtual_infrared: bool

    def __post_init__(self):
        if self.client is None:
            raise TypeError
        if self.device_id is None:
            raise TypeError

        # SwitchBot API returns FFFFFFFFFFFF or 000000000000 if there is no hub device ID
        if self.hub_device_id in ["FFFFFFFFFFFF", "000000000000"]:
            self.hub_device_id = None

    def status(self) -> DeviceStatus:
        status = self.client.devices_status(self.device_id).body
        return DeviceStatus(
            device_id=status["deviceId"] if "deviceId" in status else self.device_id,
            device_type=status["deviceType"] if "deviceType" in status else self.device_type,
            device_name=status["deviceName"] if "deviceName" in status else self.device_name,
            hub_device_id=status["hubDeviceId"] if "hubDeviceId" in status else self.hub_device_id,
            raw_data=status,
        )

    def command(
        self, command: str, parameter: str = None, command_type: str = None
    ) -> SwitchBotCommandResult:
        response = self.client.devices_commands(self.device_id, command, parameter, command_type)
        return SwitchBotCommandResult(response.status_code, response.message, response.body)

    def __repr__(self):
        data = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_name": self.device_name,
            "hub_device_id": self.hub_device_id,
            "is_virtual_infrared": self.is_virtual_infrared,
        }
        return self.__class__.__qualname__ + f"({data})"


@dataclass()
class SwitchBotCommandResult:
    status_code: int
    message: str
    response_body: dict

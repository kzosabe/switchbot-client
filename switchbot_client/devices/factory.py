from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .physical import SwitchBotPhysicalDevice
from .remote import SwitchBotRemoteDevice

if TYPE_CHECKING:
    from switchbot_client.api import SwitchBotAPIClient
    from switchbot_client.devices.base import SwitchBotDevice
    from switchbot_client.types import APIPhysicalDeviceObject, APIRemoteDeviceObject


class SwitchBotDeviceFactory:
    @staticmethod
    def create(
        client: SwitchBotAPIClient, device: Union[APIPhysicalDeviceObject, APIRemoteDeviceObject]
    ) -> SwitchBotDevice:
        if "deviceType" in device:
            return SwitchBotPhysicalDevice.create(client, device)  # type: ignore
        if "remoteType" in device:
            return SwitchBotRemoteDevice.create(client, device)  # type: ignore
        raise TypeError(f"invalid device object: {device}")

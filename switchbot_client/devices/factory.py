from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .physical import SwitchBotPhysicalDevice
from .remote import SwitchBotRemoteDevice

if TYPE_CHECKING:
    from switchbot_client import SwitchBotClient
    from switchbot_client.devices.base import SwitchBotDevice
    from switchbot_client.types import APIPhysicalDeviceObject, APIRemoteDeviceObject


class SwitchBotDeviceFactory:
    @staticmethod
    def create(
        client: SwitchBotClient,
        api_object: Union[APIPhysicalDeviceObject, APIRemoteDeviceObject],
    ) -> SwitchBotDevice:
        if "deviceType" in api_object:
            return SwitchBotPhysicalDevice.create_by_api_object(client, api_object)  # type: ignore
        if "remoteType" in api_object:
            return SwitchBotRemoteDevice.create_by_api_object(client, api_object)  # type: ignore
        raise TypeError(f"invalid device object: {api_object}")

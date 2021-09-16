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
        client: SwitchBotAPIClient,
        api_object: Union[APIPhysicalDeviceObject, APIRemoteDeviceObject],
    ) -> SwitchBotDevice:
        if "deviceType" in api_object:
            return SwitchBotPhysicalDevice.create(client, api_object)  # type: ignore
        if "remoteType" in api_object:
            return SwitchBotRemoteDevice.create(client, api_object)  # type: ignore
        raise TypeError(f"invalid device object: {api_object}")

    @staticmethod
    def create_from_device_object(
        client, api_object: Union[APIPhysicalDeviceObject, APIRemoteDeviceObject]
    ) -> SwitchBotDevice:
        if client is None:
            raise TypeError
        if api_object is None:
            raise TypeError

        device_id = api_object["deviceId"]
        device_name = api_object["deviceName"]
        hub_device_id = api_object["hubDeviceId"]

        if "deviceType" in api_object:
            device_type = api_object["deviceType"]  # type: ignore
        elif "remoteType" in api_object:
            device_type = api_object["remoteType"]  # type: ignore
        else:
            raise TypeError

        return SwitchBotDevice(client, device_id, device_type, device_name, hub_device_id)

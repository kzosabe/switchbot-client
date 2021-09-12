from __future__ import annotations

from typing import TYPE_CHECKING, Union

from switchbot_client.enums import ControlCommand
from switchbot_client.types import APIPhysicalDeviceObject, APIRemoteDeviceObject

if TYPE_CHECKING:
    from switchbot_client.client import SwitchBotAPIClient, SwitchBotAPIResponse


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

    @staticmethod
    def create(
        client: SwitchBotAPIClient, device: Union[APIPhysicalDeviceObject, APIRemoteDeviceObject]
    ):
        if "deviceType" in device:
            return SwitchBotPhysicalDevice(
                client, device["deviceId"], device["deviceType"]  # type: ignore
            )
        if "remoteType" in device:
            return SwitchBotRemoteDevice(
                client, device["deviceId"], device["remoteType"]  # type: ignore
            )
        raise TypeError(f"invalid device object: {device}")


class SwitchBotPhysicalDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str, device_type: str):
        super().__init__(client, device_id, device_type)
        self._check_device_type()

    def _check_device_type(self):
        expected_device_type = self.device_type
        status = self.client.devices_status(self.device_id)
        actual_device_type = status.body["deviceType"]
        if actual_device_type != expected_device_type:
            raise RuntimeError(
                f"Illegal device type. "
                f"expected: {expected_device_type}, actual: {actual_device_type}"
            )


class SwitchBotRemoteDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str, device_type: str):
        super().__init__(client, device_id, device_type)
        self._check_remote_type()

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.TURN_OFF)

    def _check_remote_type(self):
        expected_device_type = self.device_type
        infrared_remote_devices = self.client.devices().body["infraredRemoteList"]
        for device in infrared_remote_devices:
            if device["deviceId"] == self.device_id:
                actual_device_type = device["remoteType"]
                if actual_device_type == expected_device_type:
                    return
                raise RuntimeError(
                    f"Illegal device type. "
                    f"expected: {expected_device_type}, actual: {actual_device_type}"
                )
        raise RuntimeError(f"device not found: {self.device_id}")

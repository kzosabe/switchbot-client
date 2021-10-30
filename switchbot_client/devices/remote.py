from __future__ import annotations

from typing import TYPE_CHECKING

from switchbot_client.enums import ControlCommand, RemoteType
from switchbot_client.types import APIRemoteDeviceObject

from .base import SwitchBotCommandResult, SwitchBotDevice

if TYPE_CHECKING:
    from switchbot_client.api import SwitchBotAPIClient


class SwitchBotRemoteDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        device_id = device["deviceId"]
        remote_type = device["remoteType"]
        device_name = device["deviceName"]
        hub_device_id = device["hubDeviceId"]
        super().__init__(client, device_id, remote_type, device_name, hub_device_id, True)
        self.device = device

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.TURN_OFF)

    @staticmethod
    def create_by_api_object(  # noqa
        client: SwitchBotAPIClient, device: APIRemoteDeviceObject
    ) -> SwitchBotRemoteDevice:
        # pylint: disable=too-many-branches,too-many-return-statements
        remote_type = device["remoteType"]
        if remote_type == RemoteType.AIR_CONDITIONER:
            return AirConditioner(client, device)
        if remote_type == RemoteType.TV:
            return TV(client, device)
        if remote_type == RemoteType.LIGHT:
            return Light(client, device)
        if remote_type == RemoteType.IPTV_STREAMER:
            return IPTVStreamer(client, device)
        if remote_type == RemoteType.SET_TOP_BOX:
            return SetTopBox(client, device)
        if remote_type == RemoteType.DVD:
            return DVD(client, device)
        if remote_type == RemoteType.FAN:
            return Fan(client, device)
        if remote_type == RemoteType.PROJECTOR:
            return Projector(client, device)
        if remote_type == RemoteType.CAMERA:
            return Camera(client, device)
        if remote_type == RemoteType.AIR_PURIFIER:
            return AirPurifier(client, device)
        if remote_type == RemoteType.SPEAKER:
            return Speaker(client, device)
        if remote_type == RemoteType.WATER_HEATER:
            return WaterHeater(client, device)
        if remote_type == RemoteType.VACUUM_CLEANER:
            return VacuumCleaner(client, device)
        if remote_type == RemoteType.OTHERS:
            return Others(client, device)

        raise TypeError(f"invalid physical device object: {device}")

    @staticmethod
    def get_device_by_id(client: SwitchBotAPIClient, device_id: str) -> APIRemoteDeviceObject:
        if client is None:
            raise TypeError
        if device_id is None:
            raise TypeError
        response = client.devices()
        remote_devices = response.body["infraredRemoteList"]
        for device in remote_devices:
            if device["deviceId"] == device_id:
                return device
        raise RuntimeError

    def _check_remote_type(self, expected_device_type: str):
        if self.device_type != expected_device_type:
            raise RuntimeError(
                f"Illegal device type. "
                f"expected: {expected_device_type}, actual: {self.device_type}"
            )


class AirConditioner(SwitchBotRemoteDevice):
    class Parameters:
        MODE_AUTO = 1
        MODE_COOL = 2
        MODE_DRY = 3
        MODE_FAN = 4
        MODE_HEAT = 5
        FAN_SPEED_AUTO = 1
        FAN_SPEED_LOW = 2
        FAN_SPEED_MEDIUM = 3
        FAN_SPEED_HIGH = 4
        POWER_ON = "on"
        POWER_OFF = "off"

    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.AIR_CONDITIONER)

    def set_all(
        self, temperature: float, mode: str, fan_speed: str, power: str
    ) -> SwitchBotCommandResult:
        """
        temperature: temperature in celsius
        mode(Parameters.MODE_XXX): 1(auto), 2(cool), 3(dry), 4(fan), 5(heat)
        fan_speed(Parameters.FAN_SPEED_XXX): 1(auto), 2(low), 3(medium), 4(high);
        power(Parameters.POWER_XXX): on, off
        """
        return self.command(
            ControlCommand.VirtualInfrared.SET_ALL,
            parameter=f"{temperature},{mode},{fan_speed},{power}",
        )

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> AirConditioner:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return AirConditioner(client, device)


class TV(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.TV)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> TV:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return TV(client, device)


class Light(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.LIGHT)

    def brightness_up(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.BRIGHTNESS_UP)

    def brightness_down(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.BRIGHTNESS_DOWN)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Light:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Light(client, device)


class IPTVStreamer(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.IPTV_STREAMER)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> IPTVStreamer:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return IPTVStreamer(client, device)


class SetTopBox(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.SET_TOP_BOX)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> SetTopBox:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return SetTopBox(client, device)


class DVD(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.DVD)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> DVD:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return DVD(client, device)


class Fan(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.FAN)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Fan:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Fan(client, device)


class Projector(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.PROJECTOR)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Projector:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Projector(client, device)


class Camera(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.CAMERA)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Camera:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Camera(client, device)


class AirPurifier(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.AIR_PURIFIER)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> AirPurifier:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return AirPurifier(client, device)


class Speaker(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.SPEAKER)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Speaker:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Speaker(client, device)


class WaterHeater(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.WATER_HEATER)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> WaterHeater:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return WaterHeater(client, device)


class VacuumCleaner(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.VACUUM_CLEANER)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> VacuumCleaner:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return VacuumCleaner(client, device)


class Others(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.OTHERS)

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Others:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Others(client, device)

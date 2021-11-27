from __future__ import annotations

from typing import TYPE_CHECKING

from switchbot_client.enums import ControlCommand, RemoteType
from switchbot_client.types import APIRemoteDeviceObject

from .base import SwitchBotCommandResult, SwitchBotDevice

if TYPE_CHECKING:
    from switchbot_client import SwitchBotClient


class SwitchBotRemoteDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
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
        client: SwitchBotClient, device: APIRemoteDeviceObject
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
    def get_device_by_id(client: SwitchBotClient, device_id: str) -> APIRemoteDeviceObject:
        if client is None:
            raise TypeError
        if device_id is None:
            raise TypeError
        response = client.api_client.devices()
        remote_devices = response.body["infraredRemoteList"]
        for device in remote_devices:
            if device["deviceId"] == device_id:
                return device
        raise RuntimeError(f"device not found: {device_id}")

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

    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.AIR_CONDITIONER)

        # remote devices don't have status fetch commands
        # we can only memorize recently applied parameter and use it
        self.temperature_memory = 25.0
        self.mode_memory = AirConditioner.Parameters.MODE_AUTO
        self.fan_speed_memory = AirConditioner.Parameters.FAN_SPEED_AUTO

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> AirConditioner:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return AirConditioner(client, device)

    def set_all(
        self, temperature: float, mode: int, fan_speed: int, power: str
    ) -> SwitchBotCommandResult:
        """
        temperature: temperature in celsius
        mode(Parameters.MODE_XXX): 1(auto), 2(cool), 3(dry), 4(fan), 5(heat)
        fan_speed(Parameters.FAN_SPEED_XXX): 1(auto), 2(low), 3(medium), 4(high)
        power(Parameters.POWER_XXX): on, off
        """
        self.temperature_memory = temperature
        self.mode_memory = mode
        self.fan_speed_memory = fan_speed
        return self.command(
            ControlCommand.VirtualInfrared.SET_ALL,
            parameter=f"{temperature},{mode},{fan_speed},{power}",
        )

    def set_temperature(self, temperature: float) -> SwitchBotCommandResult:
        """
        temperature: temperature in celsius

        Note that if you have not set the mode and fan_speed in this object before,
        the following default values will be set.
        This is because it is not possible to get the current status from virtual infrared devices.
        mode: auto, fan_speed: auto

        It is recommended to turn on AirConditioner with the set_all
        with all values specified before use this function.
        """
        return self.set_all(temperature, self.mode_memory, self.fan_speed_memory, "on")

    def set_mode(self, mode: int) -> SwitchBotCommandResult:
        """
        mode(Parameters.MODE_XXX): 1(auto), 2(cool), 3(dry), 4(fan), 5(heat)

        Note that if you have not set the temperature and fan_speed in this object before,
        the following default values will be set.
        This is because it is not possible to get the current status from virtual infrared devices.
        temperature: 25, fan_speed: auto

        It is recommended to turn on AirConditioner with the set_all
        with all values specified before use this function.
        """
        return self.set_all(self.temperature_memory, mode, self.fan_speed_memory, "on")

    def set_fan_speed(self, fan_speed: int) -> SwitchBotCommandResult:
        """
        fan_speed(Parameters.FAN_SPEED_XXX): 1(auto), 2(low), 3(medium), 4(high)

        Note that if you have not set the temperature and mode in this object before,
        the following default values will be set.
        This is because it is not possible to get the current status from virtual infrared devices.
        temperature: 25, mode: auto

        It is recommended to turn on AirConditioner with the set_all
        with all values specified before use this function.
        """
        return self.set_all(self.temperature_memory, self.mode_memory, fan_speed, "on")


class TV(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.TV)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> TV:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return TV(client, device)

    def set_channel(self, channel_number: int) -> SwitchBotCommandResult:
        return self.command(
            ControlCommand.VirtualInfrared.SET_CHANNEL,
            parameter=f"{channel_number}",
        )

    def volume_add(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.VOLUME_ADD)

    def volume_sub(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.VOLUME_SUB)

    def channel_add(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.CHANNEL_ADD)

    def channel_sub(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.CHANNEL_SUB)


class Light(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.LIGHT)

    def brightness_up(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.BRIGHTNESS_UP)

    def brightness_down(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.BRIGHTNESS_DOWN)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Light:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Light(client, device)


class IPTVStreamer(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.IPTV_STREAMER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> IPTVStreamer:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return IPTVStreamer(client, device)

    def volume_add(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.VOLUME_ADD)

    def volume_sub(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.VOLUME_SUB)

    def channel_add(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.CHANNEL_ADD)

    def channel_sub(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.CHANNEL_SUB)


class SetTopBox(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.SET_TOP_BOX)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> SetTopBox:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return SetTopBox(client, device)

    def volume_add(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.VOLUME_ADD)

    def volume_sub(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.VOLUME_SUB)

    def channel_add(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.CHANNEL_ADD)

    def channel_sub(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.CHANNEL_SUB)


class DVD(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.DVD)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> DVD:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return DVD(client, device)

    def mute(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.SET_MUTE)

    def fast_forward(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.FAST_FORWARD)

    def rewind(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.REWIND)

    def next(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.NEXT)

    def previous(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.PREVIOUS)

    def pause(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.PAUSE)

    def play(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.PLAY)

    def stop(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.STOP)


class Fan(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.FAN)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Fan:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Fan(client, device)

    def swing(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.SWING)

    def timer(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.TIMER)

    def low_speed(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.LOW_SPEED)

    def middle_speed(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.MIDDLE_SPEED)

    def high_speed(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.HIGH_SPEED)


class Projector(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.PROJECTOR)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Projector:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Projector(client, device)


class Camera(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.CAMERA)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Camera:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Camera(client, device)


class AirPurifier(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.AIR_PURIFIER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> AirPurifier:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return AirPurifier(client, device)


class Speaker(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.SPEAKER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Speaker:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Speaker(client, device)

    def mute(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.SET_MUTE)

    def fast_forward(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.FAST_FORWARD)

    def rewind(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.REWIND)

    def next(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.NEXT)

    def previous(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.PREVIOUS)

    def pause(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.PAUSE)

    def play(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.PLAY)

    def stop(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.VirtualInfrared.STOP)


class WaterHeater(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.WATER_HEATER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> WaterHeater:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return WaterHeater(client, device)


class VacuumCleaner(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.VACUUM_CLEANER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> VacuumCleaner:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return VacuumCleaner(client, device)


class Others(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
        super().__init__(client, device)
        self._check_remote_type(RemoteType.OTHERS)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Others:
        device = SwitchBotRemoteDevice.get_device_by_id(client, device_id)
        return Others(client, device)

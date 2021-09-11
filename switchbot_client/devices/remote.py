from switchbot_client import (
    SwitchBotAPIClient,
    SwitchBotAPIResponse,
    RemoteType,
    ControlCommand,
)
from .physical import SwitchBotDeviceBase


class SwitchBotRemoteDevice(SwitchBotDeviceBase):
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

    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.AIR_CONDITIONER)

    def set_all(
        self, temperature: int, mode: str, fan_speed: str, power: str
    ) -> SwitchBotAPIResponse:
        """
        temperature: temperature in celsius
        mode(Parameters.MODE_XXX): 1(auto), 2(cool), 3(dry), 4(fan), 5(heat)
        fan_speed(Parameters.FAN_SPEED_XXX): 1(auto), 2(low), 3(medium), 4(high);
        power(Parameters.POWER_XXX): on, off
        """
        return self.control(
            ControlCommand.VirtualInfrared.SET_ALL,
            parameter=f"{temperature},{mode},{fan_speed},{power}",
        )


class TV(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.TV)


class Light(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.LIGHT)

    def brightness_up(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.BRIGHTNESS_UP)

    def brightness_down(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.BRIGHTNESS_DOWN)


class IPTVStreamer(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.IPTV_STREAMER)


class SetTopBox(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.SET_TOP_BOX)


class DVD(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.DVD)


class Fan(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.FAN)


class Projector(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.PROJECTOR)


class Camera(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.CAMERA)


class AirPurifier(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.AIR_PURIFIER)


class Speaker(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.SPEAKER)


class WaterHeater(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.WATER_HEATER)


class VacuumCleaner(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.VACUUM_CLEANER)


class Others(SwitchBotRemoteDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, RemoteType.OTHERS)

from switchbot_client import (
    SwitchBotAPIClient,
    SwitchBotAPIResponse,
    DeviceType,
    ControlCommand,
)


class SwitchBotDeviceBase:
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


class SwitchBotDevice(SwitchBotDeviceBase):
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


class Hub(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUB)


class HubMini(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUB_MINI)


class HubPlus(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUB_PLUS)


class Bot(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.BOT)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_OFF)

    def press(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.PRESS)


class Plug(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.PLUG)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_OFF)


class Curtain(SwitchBotDevice):
    class Parameters:
        MODE_PERFORMANCE = "0"
        MODE_SILENT = "1"
        MODE_DEFAULT = "ff"

    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.CURTAIN)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Curtain.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Curtain.TURN_OFF)

    def set_position(self, index: int, mode: str, position: int) -> SwitchBotAPIResponse:
        """
        mode(Parameters.MODE_XXX): 0 (Performance Mode), 1 (Silent Mode), ff (default mode)
        position: 0 ~ 100 (0 means opened, 100 means closed)
        """
        return self.control(
            ControlCommand.Curtain.SET_POSITION, parameter=f"{index},{mode},{position}"
        )


class Meter(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.METER)


class Humidifier(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUMIDIFIER)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Humidifier.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Humidifier.TURN_OFF)

    def set_mode(self, mode: str) -> SwitchBotAPIResponse:
        """
        auto or 101 or 102 or 103 or {0~100}
        auto: set to Auto Mode
        101: set atomization efficiency to 34%
        102: set atomization efficiency to 67%
        103: set atomization efficiency to 100%
        """
        return self.control(ControlCommand.Humidifier.SET_MODE, parameter=mode)


class SmartFan(SwitchBotDevice):
    class Parameters:
        POWER_ON = "on"
        POWER_OFF = "off"
        FAN_MODE_STANDARD = 1
        FAN_MODE_NATURAL = 2

    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.SMART_FAN)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.SmartFan.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.SmartFan.TURN_OFF)

    def set_all_status(
        self, power: str, fan_mode: int, fan_speed: int, shake_range: int
    ) -> SwitchBotAPIResponse:
        """
        power(Parameters.POWER_XXX): off, on
        fan_mode(Parameters.FAN_MODE_XXX): 1 (Standard), 2 (Natural)
        fan_speed: 1, 2, 3, 4
        shake_range: 0 ~ 120
        """
        return self.control(
            ControlCommand.SmartFan.SET_ALL_STATUS,
            parameter=f"{power},{fan_mode},{fan_speed},{shake_range}",
        )


class IndoorCam(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.INDOOR_CAM)

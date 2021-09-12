from __future__ import annotations

from typing import TYPE_CHECKING

from switchbot_client.enums import ControlCommand, DeviceType

from .base import SwitchBotPhysicalDevice

if TYPE_CHECKING:
    from switchbot_client.client import SwitchBotAPIClient, SwitchBotAPIResponse


class Hub(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUB)


class HubMini(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUB_MINI)


class HubPlus(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.HUB_PLUS)


class Bot(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.BOT)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_OFF)

    def press(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.PRESS)


class Plug(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.PLUG)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_OFF)


class Curtain(SwitchBotPhysicalDevice):
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


class Meter(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.METER)


class MotionSensor(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.MOTION_SENSOR)


class ContactSensor(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.CONTACT_SENSOR)


class ColorBulb(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.COLOR_BULB)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Humidifier.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Humidifier.TURN_OFF)

    def set_brightness(self, brightness: int) -> SwitchBotAPIResponse:
        """
        brightness: 1 ~ 100
        """
        return self.control(ControlCommand.ColorBulb.SET_BRIGHTNESS, parameter=f"{brightness}")

    def set_color(self, red: int, green: int, blue: int) -> SwitchBotAPIResponse:
        """
        red: 0 ~ 255
        green: 0 ~ 255
        blue: 0 ~ 255
        """
        return self.control(ControlCommand.ColorBulb.SET_COLOR, parameter=f"{red}:{green}:{blue}")

    def set_color_temperature(self, temperature: int) -> SwitchBotAPIResponse:
        """
        temperature: 2700 ~ 6500
        """
        return self.control(
            ControlCommand.ColorBulb.SET_COLOR_TEMPERATURE, parameter=f"{temperature}"
        )


class Humidifier(SwitchBotPhysicalDevice):
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


class SmartFan(SwitchBotPhysicalDevice):
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


class IndoorCam(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id, DeviceType.INDOOR_CAM)

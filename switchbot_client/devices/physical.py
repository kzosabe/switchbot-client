from __future__ import annotations

from typing import TYPE_CHECKING

from switchbot_client.enums import ControlCommand, DeviceType
from switchbot_client.types import APIPhysicalDeviceObject

from .base import SwitchBotDevice

if TYPE_CHECKING:
    from switchbot_client.api import SwitchBotAPIClient, SwitchBotAPIResponse


class SwitchBotPhysicalDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device: APIPhysicalDeviceObject):
        device_id = device["deviceId"]
        device_type = device["deviceType"]
        device_name = device["deviceName"]
        hub_device_id = device["hubDeviceId"]
        super().__init__(client, device_id, device_type, device_name, hub_device_id)
        self._check_device_type()

    @staticmethod
    def create(  # noqa
        client: SwitchBotAPIClient, device: APIPhysicalDeviceObject
    ) -> SwitchBotPhysicalDevice:
        # pylint: disable=too-many-branches,too-many-return-statements
        device_type = device["deviceType"]
        if device_type == DeviceType.HUB:
            return Hub(client, device)
        if device_type == DeviceType.HUB_MINI:
            return HubMini(client, device)
        if device_type == DeviceType.HUB_PLUS:
            return HubPlus(client, device)
        if device_type == DeviceType.BOT:
            return Bot(client, device)
        if device_type == DeviceType.PLUG:
            return Plug(client, device)
        if device_type == DeviceType.CURTAIN:
            return Curtain(client, device)
        if device_type == DeviceType.METER:
            return Meter(client, device)
        if device_type == DeviceType.MOTION_SENSOR:
            return MotionSensor(client, device)
        if device_type == DeviceType.CONTACT_SENSOR:
            return ContactSensor(client, device)
        if device_type == DeviceType.COLOR_BULB:
            return ColorBulb(client, device)
        if device_type == DeviceType.HUMIDIFIER:
            return Humidifier(client, device)
        if device_type == DeviceType.SMART_FAN:
            return SmartFan(client, device)
        if device_type == DeviceType.INDOOR_CAM:
            return IndoorCam(client, device)

        raise TypeError(f"invalid physical device object: {device}")

    @staticmethod
    def get_device_by_id(client: SwitchBotAPIClient, device_id: str) -> APIPhysicalDeviceObject:
        response = client.devices()
        physical_devices = response.body["deviceList"]
        for device in physical_devices:
            if device["deviceId"] == device_id:
                return device
        raise RuntimeError

    def _check_device_type(self):
        expected_device_type = self.device_type
        status = self.client.devices_status(self.device_id)
        # some device returns empty body for devices_status
        if status.body == {}:
            return
        actual_device_type = status.body["deviceType"]
        if actual_device_type != expected_device_type:
            raise RuntimeError(
                f"Illegal device type. "
                f"expected: {expected_device_type}, actual: {actual_device_type}"
            )


class Hub(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Hub:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Hub(client, device)


class HubMini(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> HubMini:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return HubMini(client, device)


class HubPlus(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> HubPlus:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return HubPlus(client, device)


class Bot(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Bot:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Bot(client, device)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_OFF)

    def press(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.PRESS)


class Plug(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Plug:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Plug(client, device)

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_OFF)


class Curtain(SwitchBotPhysicalDevice):
    class Parameters:
        MODE_PERFORMANCE = "0"
        MODE_SILENT = "1"
        MODE_DEFAULT = "ff"

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Curtain:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Curtain(client, device)

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
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Meter:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Meter(client, device)


class MotionSensor(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> MotionSensor:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return MotionSensor(client, device)


class ContactSensor(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> ContactSensor:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return ContactSensor(client, device)


class ColorBulb(SwitchBotPhysicalDevice):
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> ColorBulb:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return ColorBulb(client, device)

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
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> Humidifier:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Humidifier(client, device)

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

    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> SmartFan:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return SmartFan(client, device)

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
    @staticmethod
    def create_by_id(client: SwitchBotAPIClient, device_id: str) -> IndoorCam:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return IndoorCam(client, device)

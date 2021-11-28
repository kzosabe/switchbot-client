from __future__ import annotations

from typing import TYPE_CHECKING

from switchbot_client.devices.status import (
    BotDeviceStatus,
    ColorBulbDeviceStatus,
    ContactSensorDeviceStatus,
    CurtainDeviceStatus,
    DeviceStatus,
    HumidifierDeviceStatus,
    MeterDeviceStatus,
    MotionSensorDeviceStatus,
    PlugDeviceStatus,
    SmartFanDeviceStatus,
)
from switchbot_client.enums import ControlCommand, DeviceType
from switchbot_client.types import APIPhysicalDeviceObject

from .base import SwitchBotCommandResult, SwitchBotDevice

if TYPE_CHECKING:
    from switchbot_client import SwitchBotClient


class SwitchBotPhysicalDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        device_id = device["deviceId"]
        device_type = device["deviceType"]
        device_name = device["deviceName"]
        hub_device_id = device["hubDeviceId"]
        super().__init__(client, device_id, device_type, device_name, hub_device_id, False)
        self.device = device

    @staticmethod
    def create_by_api_object(  # noqa
        client: SwitchBotClient, device: APIPhysicalDeviceObject
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
        if device_type == DeviceType.REMOTE:
            return Remote(client, device)

        raise TypeError(f"invalid physical device object: {device}")

    @staticmethod
    def get_device_by_id(client: SwitchBotClient, device_id: str) -> APIPhysicalDeviceObject:
        if client is None:
            raise TypeError
        if device_id is None:
            raise TypeError
        response = client.api_client.devices()
        physical_devices = response.body["deviceList"]
        for device in physical_devices:
            if device["deviceId"] == device_id:
                return device
        raise RuntimeError(f"device not found: {device_id}")

    def status(self) -> DeviceStatus:
        status = self.client.api_client.devices_status(self.device_id).body
        return DeviceStatus(
            device_id=status["deviceId"] if "deviceId" in status else self.device_id,
            device_type=status["deviceType"] if "deviceType" in status else self.device_type,
            device_name=status["deviceName"] if "deviceName" in status else self.device_name,
            hub_device_id=status["hubDeviceId"] if "hubDeviceId" in status else self.hub_device_id,
            raw_data=status,
        )

    def _check_device_type(self, expected_device_type: str):
        if self.device_type != expected_device_type:
            raise RuntimeError(
                f"Illegal device type. "
                f"expected: {expected_device_type}, actual: {self.device_type}"
            )


class Hub(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.HUB)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Hub:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Hub(client, device)


class HubMini(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.HUB_MINI)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> HubMini:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return HubMini(client, device)


class HubPlus(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.HUB_PLUS)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> HubPlus:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return HubPlus(client, device)


class Bot(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.BOT)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Bot:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Bot(client, device)

    def status(self) -> BotDeviceStatus:
        status = super().status()
        return BotDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            power=status.raw_data["power"],
        )

    def power(self) -> str:
        return self.status().power

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Bot.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Bot.TURN_OFF)

    def press(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Bot.PRESS)


class Plug(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.PLUG)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Plug:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Plug(client, device)

    def status(self) -> PlugDeviceStatus:
        status = super().status()
        return PlugDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            power=status.raw_data["power"],
        )

    def power(self) -> str:
        return self.status().power

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Plug.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Plug.TURN_OFF)


class Curtain(SwitchBotPhysicalDevice):
    class Parameters:
        MODE_PERFORMANCE = "0"
        MODE_SILENT = "1"
        MODE_DEFAULT = "ff"

    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.CURTAIN)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Curtain:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Curtain(client, device)

    def status(self) -> CurtainDeviceStatus:
        status = super().status()
        return CurtainDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            is_calibrated=status.raw_data["calibrate"],
            is_grouped=status.raw_data["group"],
            is_moving=status.raw_data["moving"],
            slide_position=status.raw_data["slide_position"],
        )

    def slide_position(self) -> int:
        return self.status().slide_position

    def is_calibrated(self) -> bool:
        return self.status().is_calibrated

    def is_grouped(self) -> bool:
        return self.status().is_grouped

    def is_moving(self) -> bool:
        return self.status().is_moving

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Curtain.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Curtain.TURN_OFF)

    def set_position(self, index: int, mode: str, position: int) -> SwitchBotCommandResult:
        """
        mode(Parameters.MODE_XXX): 0 (Performance Mode), 1 (Silent Mode), ff (default mode)
        position: 0 ~ 100 (0 means opened, 100 means closed)
        """
        return self.command(
            ControlCommand.Curtain.SET_POSITION, parameter=f"{index},{mode},{position}"
        )


class Meter(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.METER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Meter:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Meter(client, device)

    def status(self) -> MeterDeviceStatus:
        status = super().status()
        return MeterDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            humidity=status.raw_data["humidity"],
            temperature=float(status.raw_data["temperature"]),
        )

    def temperature(self) -> float:
        return self.status().temperature

    def humidity(self) -> int:
        return self.status().humidity


class MotionSensor(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.MOTION_SENSOR)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> MotionSensor:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return MotionSensor(client, device)

    def status(self) -> MotionSensorDeviceStatus:
        status = super().status()
        return MotionSensorDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            is_move_detected=status.raw_data["moveDetected"],
            brightness=status.raw_data["brightness"],
        )

    def brightness(self) -> str:
        return self.status().brightness

    def is_move_detected(self) -> bool:
        return self.status().is_move_detected


class ContactSensor(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.CONTACT_SENSOR)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> ContactSensor:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return ContactSensor(client, device)

    def status(self) -> ContactSensorDeviceStatus:
        status = super().status()
        return ContactSensorDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            is_move_detected=status.raw_data["moveDetected"],
            brightness=status.raw_data["brightness"],
            open_state=status.raw_data["openState"],
        )

    def brightness(self) -> str:
        return self.status().brightness

    def open_state(self) -> str:
        return self.status().open_state

    def is_move_detected(self) -> bool:
        return self.status().is_move_detected


class ColorBulb(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.COLOR_BULB)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> ColorBulb:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return ColorBulb(client, device)

    def status(self) -> ColorBulbDeviceStatus:
        status = super().status()
        colors = [int(i) for i in status.raw_data["color"].split(":")]
        color_hex = f"#{colors[0]:02x}{colors[1]:02x}{colors[2]:02x}"
        return ColorBulbDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            power=status.raw_data["power"],
            color_hex=color_hex,
            color_temperature=status.raw_data["colorTemperature"],
            brightness=status.raw_data["brightness"],
        )

    def power(self) -> str:
        return self.status().power

    def brightness(self) -> int:
        return self.status().brightness

    def color_hex(self) -> str:
        """
        returns #rrggbb format color string
        """
        return self.status().color_hex

    def color_temperature(self) -> int:
        return self.status().color_temperature

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Humidifier.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Humidifier.TURN_OFF)

    def set_brightness(self, brightness: int) -> SwitchBotCommandResult:
        """
        brightness: 1 ~ 100
        """
        return self.command(ControlCommand.ColorBulb.SET_BRIGHTNESS, parameter=f"{brightness}")

    def set_color_by_number(self, red: int, green: int, blue: int) -> SwitchBotCommandResult:
        """
        red: 0 ~ 255
        green: 0 ~ 255
        blue: 0 ~ 255
        """
        return self.command(ControlCommand.ColorBulb.SET_COLOR, parameter=f"{red}:{green}:{blue}")

    def set_color(self, color_hex: str) -> SwitchBotCommandResult:
        rgb = tuple(int(color_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        return self.set_color_by_number(rgb[0], rgb[1], rgb[2])

    def set_color_temperature(self, temperature: int) -> SwitchBotCommandResult:
        """
        temperature: 2700 ~ 6500
        """
        return self.command(
            ControlCommand.ColorBulb.SET_COLOR_TEMPERATURE, parameter=f"{temperature}"
        )


class Humidifier(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.HUMIDIFIER)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Humidifier:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Humidifier(client, device)

    def status(self) -> HumidifierDeviceStatus:
        status = super().status()
        return HumidifierDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            power=status.raw_data["power"],
            humidity=status.raw_data["humidity"],
            temperature=float(status.raw_data["temperature"]),
            atomization_efficiency=status.raw_data["nebulizationEfficiency"],
            is_auto=status.raw_data["auto"],
            is_child_lock=status.raw_data["childLock"],
            is_muted=not status.raw_data["sound"],
            is_lack_water=status.raw_data["lackWater"],
        )

    def power(self) -> str:
        return self.status().power

    def temperature(self) -> float:
        return self.status().temperature

    def humidity(self) -> int:
        return self.status().humidity

    def atomization_efficiency(self) -> int:
        return self.status().atomization_efficiency

    def is_auto(self) -> bool:
        return self.status().is_auto

    def is_child_lock(self) -> bool:
        return self.status().is_child_lock

    def is_muted(self) -> bool:
        return not self.status().is_muted

    def is_lack_water(self) -> bool:
        return not self.status().is_lack_water

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Humidifier.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.Humidifier.TURN_OFF)

    def set_mode(self, mode: str) -> SwitchBotCommandResult:
        """
        auto or 101 or 102 or 103 or {0~100}
        auto: set to Auto Mode
        101: set atomization efficiency to 34%
        102: set atomization efficiency to 67%
        103: set atomization efficiency to 100%
        """
        return self.command(ControlCommand.Humidifier.SET_MODE, parameter=mode)

    def set_atomization_efficiency(self, percentage: int) -> SwitchBotCommandResult:
        return self.set_mode(str(percentage))

    def set_auto_mode(self) -> SwitchBotCommandResult:
        return self.set_mode("auto")


class SmartFan(SwitchBotPhysicalDevice):
    class Parameters:
        POWER_ON = "on"
        POWER_OFF = "off"
        FAN_MODE_STANDARD = 1
        FAN_MODE_NATURAL = 2

    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.SMART_FAN)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> SmartFan:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return SmartFan(client, device)

    def status(self) -> SmartFanDeviceStatus:
        status = super().status()
        return SmartFanDeviceStatus(
            device_id=status.device_id,
            device_type=status.device_type,
            device_name=status.device_name,
            hub_device_id=status.hub_device_id,
            raw_data=status.raw_data,
            mode=status.raw_data["mode"],
            speed=status.raw_data["speed"],
            is_shaking=status.raw_data["shaking"],
            shake_center=status.raw_data["shakeCenter"],
            shake_range=status.raw_data["shakeRange"],
        )

    def mode(self) -> int:
        return self.status().mode

    def speed(self) -> int:
        return self.status().speed

    def shake_center(self) -> int:
        return self.status().shake_center

    def shake_range(self) -> int:
        return self.status().shake_range

    def is_shaking(self) -> bool:
        return self.status().is_shaking

    def turn_on(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.SmartFan.TURN_ON)

    def turn_off(self) -> SwitchBotCommandResult:
        return self.command(ControlCommand.SmartFan.TURN_OFF)

    def set_all_status(
        self, power: str, fan_mode: int, fan_speed: int, shake_range: int
    ) -> SwitchBotCommandResult:
        """
        power(Parameters.POWER_XXX): off, on
        fan_mode(Parameters.FAN_MODE_XXX): 1 (Standard), 2 (Natural)
        fan_speed: 1, 2, 3, 4
        shake_range: 0 ~ 120
        """
        return self.command(
            ControlCommand.SmartFan.SET_ALL_STATUS,
            parameter=f"{power},{fan_mode},{fan_speed},{shake_range}",
        )

    def set_fan_mode(self, fan_mode: int) -> SwitchBotCommandResult:
        """
        fan_mode(Parameters.FAN_MODE_XXX): 1 (Standard), 2 (Natural)
        """
        data = self.status().raw_data
        fan_speed = data["speed"]
        shake_range = data["shakeRange"]
        return self.command(
            ControlCommand.SmartFan.SET_ALL_STATUS,
            parameter=f"on,{fan_mode},{fan_speed},{shake_range}",
        )

    def set_fan_speed(self, fan_speed: int) -> SwitchBotCommandResult:
        """
        fan_speed: 1, 2, 3, 4
        """
        data = self.status().raw_data
        fan_mode = data["mode"]
        shake_range = data["shakeRange"]
        return self.command(
            ControlCommand.SmartFan.SET_ALL_STATUS,
            parameter=f"on,{fan_mode},{fan_speed},{shake_range}",
        )

    def set_shake_range(self, shake_range: int) -> SwitchBotCommandResult:
        """
        shake_range: 0 ~ 120
        """
        data = self.status().raw_data
        fan_mode = data["mode"]
        fan_speed = data["speed"]
        return self.command(
            ControlCommand.SmartFan.SET_ALL_STATUS,
            parameter=f"on,{fan_mode},{fan_speed},{shake_range}",
        )


class IndoorCam(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.INDOOR_CAM)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> IndoorCam:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return IndoorCam(client, device)


class Remote(SwitchBotPhysicalDevice):
    def __init__(self, client: SwitchBotClient, device: APIPhysicalDeviceObject):
        super().__init__(client, device)
        self._check_device_type(DeviceType.REMOTE)

    @staticmethod
    def create_by_id(client: SwitchBotClient, device_id: str) -> Remote:
        device = SwitchBotPhysicalDevice.get_device_by_id(client, device_id)
        return Remote(client, device)

from dataclasses import dataclass
from typing import Optional


@dataclass()
class DeviceStatus:
    device_id: str
    device_type: str
    device_name: str
    hub_device_id: Optional[str]
    raw_data: dict

    def __post_init__(self):
        if self.device_type is None:
            raise TypeError
        if self.device_id is None:
            raise TypeError
        if self.device_name is None:
            raise TypeError

        # SwitchBot API returns FFFFFFFFFFFF or 000000000000 if there is no hub device ID
        if self.hub_device_id in ["FFFFFFFFFFFF", "000000000000"]:
            self.hub_device_id = None


@dataclass()
class BotDeviceStatus(DeviceStatus):
    power: str


@dataclass()
class PlugDeviceStatus(DeviceStatus):
    power: str


@dataclass()
class PlugMiniUsDeviceStatus(DeviceStatus):
    power: str
    voltage: int
    weight: int
    electricity_of_day: int
    electric_current: int


@dataclass()
class PlugMiniJpDeviceStatus(DeviceStatus):
    power: str
    voltage: int
    weight: int
    electricity_of_day: int
    electric_current: int


@dataclass()
class CurtainDeviceStatus(DeviceStatus):
    is_calibrated: bool
    is_grouped: bool
    is_moving: bool
    slide_position: int


@dataclass()
class HumidifierDeviceStatus(DeviceStatus):
    power: str
    humidity: int
    temperature: float
    atomization_efficiency: int
    is_auto: bool
    is_child_lock: bool
    is_muted: bool
    is_lack_water: bool


@dataclass()
class ColorBulbDeviceStatus(DeviceStatus):
    power: str
    color_hex: str
    color_temperature: int
    brightness: int


@dataclass()
class SmartFanDeviceStatus(DeviceStatus):
    power: str
    mode: int
    speed: int
    is_shaking: bool
    shake_center: int
    shake_range: int


@dataclass()
class StripLightDeviceStatus(DeviceStatus):
    power: str
    color_hex: str
    brightness: int


@dataclass()
class MeterDeviceStatus(DeviceStatus):
    humidity: int
    temperature: float


@dataclass()
class MeterPlusUsDeviceStatus(DeviceStatus):
    humidity: int
    temperature: float


@dataclass()
class MeterPlusJpDeviceStatus(DeviceStatus):
    humidity: int
    temperature: float


@dataclass()
class MotionSensorDeviceStatus(DeviceStatus):
    is_move_detected: bool
    brightness: str


@dataclass()
class ContactSensorDeviceStatus(DeviceStatus):
    is_move_detected: bool
    brightness: str
    open_state: str


@dataclass()
class LockDeviceStatus(DeviceStatus):
    is_calibrated: bool
    lock_state: str
    door_state: str


@dataclass()
class RobotVacuumCleanerDeviceStatus(DeviceStatus):
    working_status: str
    online_status: str
    battery: int


@dataclass
class PseudoRemoteDeviceStatus(DeviceStatus):
    power: Optional[str]

    def set_power(self, power: str):
        self.power = power
        self.raw_data["power"] = power


@dataclass
class PseudoAirConditionerStatus(PseudoRemoteDeviceStatus):
    power: Optional[str]
    temperature: Optional[float]
    mode: Optional[int]
    fan_speed: Optional[int]

    def set_temperature(self, temperature: float):
        self.temperature = temperature
        self.raw_data["temperature"] = temperature

    def set_mode(self, mode: int):
        self.mode = mode
        self.raw_data["mode"] = mode

    def set_fan_speed(self, fan_speed: int):
        self.fan_speed = fan_speed
        self.raw_data["fanSpeed"] = fan_speed

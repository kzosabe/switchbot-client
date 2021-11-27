from dataclasses import dataclass


@dataclass()
class DeviceStatus:
    device_id: str
    device_type: str
    device_name: str
    hub_device_id: str
    raw_data: dict


@dataclass()
class BotDeviceStatus(DeviceStatus):
    power: str


@dataclass()
class PlugDeviceStatus(DeviceStatus):
    power: str


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
    mode: int
    speed: int
    is_shaking: bool
    shake_center: int
    shake_range: int


@dataclass()
class MeterDeviceStatus(DeviceStatus):
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

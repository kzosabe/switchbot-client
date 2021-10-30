from dataclasses import dataclass


@dataclass()
class DeviceStatus:
    device_id: str
    device_type: str
    device_name: str
    hub_device_id: str
    raw_data: dict

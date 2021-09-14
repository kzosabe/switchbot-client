from typing_extensions import TypedDict


class APIPhysicalDeviceObject(TypedDict):
    deviceId: str
    deviceName: str
    deviceType: str
    enableCloudService: bool
    hubDeviceId: str


class APIRemoteDeviceObject(TypedDict):
    deviceId: str
    deviceName: str
    remoteType: str
    hubDeviceId: str

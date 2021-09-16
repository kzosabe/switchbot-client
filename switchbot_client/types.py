from typing_extensions import TypedDict


class APIDeviceObject(TypedDict):
    deviceId: str
    deviceName: str
    hubDeviceId: str


class APIPhysicalDeviceObject(APIDeviceObject):
    deviceType: str
    enableCloudService: bool


class APIRemoteDeviceObject(APIDeviceObject):
    remoteType: str

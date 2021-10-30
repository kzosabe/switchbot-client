import requests

from switchbot_client.client import SwitchBotClient
from switchbot_client.devices import (
    AirConditioner,
    HubMini,
    Light,
    Meter,
    SwitchBotPhysicalDevice,
    SwitchBotRemoteDevice,
)


def test_devices(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                "statusCode": 100,
                "message": "success",
                "body": {
                    "deviceList": [
                        {
                            "deviceId": "ABCDEFG",
                            "deviceName": "Meter 0A",
                            "deviceType": "Meter",
                            "enableCloudService": True,
                            "hubDeviceId": "ABCDE",
                        },
                        {
                            "deviceId": "ABCDE",
                            "deviceName": "Hub Mini 0",
                            "deviceType": "Hub Mini",
                            "hubDeviceId": "ABCDE",
                        },
                    ],
                    "infraredRemoteList": [
                        {
                            "deviceId": "12345",
                            "deviceName": "My Light",
                            "remoteType": "Light",
                            "hubDeviceId": "ABCDE",
                        },
                        {
                            "deviceId": "12345",
                            "deviceName": "My Air Conditioner",
                            "remoteType": "Air Conditioner",
                            "hubDeviceId": "ABCDE",
                        },
                    ],
                },
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    def dummy_method(self, *args):
        pass

    monkeypatch.setattr(SwitchBotPhysicalDevice, "_check_device_type", dummy_method)
    monkeypatch.setattr(SwitchBotRemoteDevice, "_check_remote_type", dummy_method)
    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotClient("token")
    sut = client.devices()
    assert sorted([type(e) for e in sut], key=lambda e: e.__name__) == [
        AirConditioner,
        HubMini,
        Light,
        Meter,
    ]

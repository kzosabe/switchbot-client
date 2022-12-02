import pytest
import requests

from switchbot_client.client import SwitchBotClient
from switchbot_client.devices import (
    AirConditioner,
    HubMini,
    Light,
    Meter,
    SwitchBotPhysicalDevice,
    SwitchBotRemoteDevice, MeterPlus,
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
                            "deviceId": "ABCDEFGH",
                            "deviceName": "Meter Plus 0A",
                            "deviceType": "MeterPlus",
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
                            "deviceId": "23456",
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
        MeterPlus,
    ]


def test_device(monkeypatch):
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
                            "deviceId": "23456",
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
    sut = client.device("12345")
    assert sut.device_name == "My Light"
    sut = client.device("some_not_exists_id")
    assert sut is None


def test_device_error_dups(monkeypatch):
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
                            "deviceId": "ABCDEFG",
                            "deviceName": "Hub Mini 0",
                            "deviceType": "Hub Mini",
                            "hubDeviceId": "ABCDE",
                        },
                    ],
                    "infraredRemoteList": [],
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
    with pytest.raises(RuntimeError):
        sut = client.device("ABCDEFG")


def test_scenes(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                "statusCode": 100,
                "message": "success",
                "body": [
                    {"sceneId": "T02-20200804130110", "sceneName": "Close Office Devices"},
                    {"sceneId": "T02-202009221414-48924101", "sceneName": "Set Office AC to 25"},
                    {"sceneId": "T02-202011051830-39363561", "sceneName": "Set Bedroom to 24"},
                ],
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    def dummy_method(self, *args):
        pass

    monkeypatch.setattr(SwitchBotPhysicalDevice, "_check_device_type", dummy_method)
    monkeypatch.setattr(SwitchBotRemoteDevice, "_check_remote_type", dummy_method)
    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotClient("token")
    sut = client.scenes()
    assert [e.scene_id for e in sut] == [
        "T02-20200804130110",
        "T02-202009221414-48924101",
        "T02-202011051830-39363561",
    ]


def test_scene(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                "statusCode": 100,
                "message": "success",
                "body": [
                    {"sceneId": "T02-20200804130110", "sceneName": "Close Office Devices"},
                    {"sceneId": "T02-202009221414-48924101", "sceneName": "Set Office AC to 25"},
                    {"sceneId": "T02-202011051830-39363561", "sceneName": "Set Bedroom to 24"},
                ],
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    def dummy_method(self, *args):
        pass

    monkeypatch.setattr(SwitchBotPhysicalDevice, "_check_device_type", dummy_method)
    monkeypatch.setattr(SwitchBotRemoteDevice, "_check_remote_type", dummy_method)
    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotClient("token")
    sut = client.scene("T02-202009221414-48924101")
    assert sut.scene_name == "Set Office AC to 25"
    sut = client.scene("some_not_exists_id")
    assert sut is None


def test_scene_error_dups(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                "statusCode": 100,
                "message": "success",
                "body": [
                    {"sceneId": "T02-20200804130110", "sceneName": "Close Office Devices"},
                    {"sceneId": "T02-20200804130110", "sceneName": "Set Office AC to 25"},
                    {"sceneId": "T02-20200804130110", "sceneName": "Set Bedroom to 24"},
                ],
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    def dummy_method(self, *args):
        pass

    monkeypatch.setattr(SwitchBotPhysicalDevice, "_check_device_type", dummy_method)
    monkeypatch.setattr(SwitchBotRemoteDevice, "_check_remote_type", dummy_method)
    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotClient("token")
    with pytest.raises(RuntimeError):
        sut = client.scene("T02-20200804130110")

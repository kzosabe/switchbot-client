import inspect

import pytest

from switchbot_client import ControlCommand, DeviceType, RemoteType
from switchbot_client.client import SwitchBotAPIClient, SwitchBotAPIResponse
from switchbot_client.devices import (
    Bot,
    Light,
    SwitchBotPhysicalDevice,
    SwitchBotRemoteDevice,
    physical,
    remote,
)


def test_all_devices_defined(monkeypatch):
    client = SwitchBotAPIClient("token")

    def dummy_method(self):
        pass

    monkeypatch.setattr(SwitchBotPhysicalDevice, "_check_device_type", dummy_method)
    monkeypatch.setattr(SwitchBotRemoteDevice, "_check_remote_type", dummy_method)

    physical_types = [getattr(DeviceType, a) for a in dir(DeviceType()) if not a.startswith("_")]
    defined_physicals = [
        a[1]
        for a in inspect.getmembers(physical, inspect.isclass)
        if issubclass(a[1], SwitchBotPhysicalDevice) and a[0] != "SwitchBotPhysicalDevice"
    ]
    defined_physicals_types = []
    for cls in defined_physicals:
        t = cls(client, "dummy").device_type
        assert t in physical_types
        defined_physicals_types.append(t)
    for t in physical_types:
        assert t in defined_physicals_types

    remote_types = [getattr(RemoteType, a) for a in dir(RemoteType()) if not a.startswith("_")]
    defined_remotes = [
        a[1]
        for a in inspect.getmembers(remote, inspect.isclass)
        if issubclass(a[1], SwitchBotRemoteDevice) and a[0] != "SwitchBotRemoteDevice"
    ]
    defined_remotes_types = []
    for cls in defined_remotes:
        t = cls(client, "dummy").device_type
        assert t in remote_types
        defined_remotes_types.append(t)
    for t in remote_types:
        assert t in defined_remotes_types


def test_init_no_client():
    with pytest.raises(TypeError):
        Bot(client=None, device_id="device_id")


def test_init_no_device_id():
    with pytest.raises(TypeError):
        client = SwitchBotAPIClient("token")
        Bot(client, None)


def test_illegal_device_type(monkeypatch):
    def mock_get(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={
                "deviceId": "ABCDE",
                "deviceType": "Meter",
                "hubDeviceId": "ABCDE",
                "humidity": 50,
                "temperature": 25.0,
            },
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices_status", mock_get)

    with pytest.raises(RuntimeError):
        client = SwitchBotAPIClient("token")
        Bot(client, "device_id")


def test_virtual_infrared_no_device(monkeypatch):
    def mock_devices(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={"infraredRemoteList": []},
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)

    with pytest.raises(RuntimeError):
        client = SwitchBotAPIClient("token")
        Light(client, "00-202001010000-12345678")


def test_virtual_infrared_illegal_device_type(monkeypatch):
    def mock_devices(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={
                "infraredRemoteList": [
                    {
                        "deviceId": "00-202001010000-12345678",
                        "deviceName": "My Air Conditioner",
                        "remoteType": "Air Conditioner",
                        "hubDeviceId": "D12345678901",
                    },
                ]
            },
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)

    with pytest.raises(RuntimeError):
        client = SwitchBotAPIClient("token")
        Light(client, "00-202001010000-12345678")


def test_light(monkeypatch):
    client = SwitchBotAPIClient("token")

    def mock_devices(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={
                "infraredRemoteList": [
                    {
                        "deviceId": "00-202001010000-12345678",
                        "deviceName": "My Light",
                        "remoteType": "Light",
                        "hubDeviceId": "D12345678901",
                    },
                ]
            },
        )

    def mock_devices_commands(
        self,
        device_id: str,
        command: str,
        parameter: str = None,
        command_type: str = None,
    ):
        assert self == client
        assert device_id == "00-202001010000-12345678"
        assert command == ControlCommand.VirtualInfrared.TURN_ON
        assert parameter is None
        assert command_type is None
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={},
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)
    monkeypatch.setattr(SwitchBotAPIClient, "devices_commands", mock_devices_commands)

    device = Light(client, "00-202001010000-12345678")
    result = device.turn_on()
    assert result.message == "success"

import pytest

from switchbot_client import ControlCommand
from switchbot_client.api import SwitchBotAPIClient, SwitchBotAPIResponse
from switchbot_client.devices import Bot, Light
from switchbot_client.types import APIPhysicalDeviceObject


def test_init_no_client():
    device = APIPhysicalDeviceObject(
        deviceId="",
        deviceName="",
        hubDeviceId="",
        deviceType="",
        enableCloudService=True,
    )
    with pytest.raises(TypeError):
        Bot(client=None, device=device)


def test_init_no_device():
    with pytest.raises(TypeError):
        client = SwitchBotAPIClient("token")
        Bot(client, None)


def test_create_no_client():
    with pytest.raises(TypeError):
        Bot.create_by_id(client=None, device_id="id")


def test_create_no_device_id():
    with pytest.raises(TypeError):
        client = SwitchBotAPIClient("token")
        Bot.create_by_id(client=client, device_id=None)


def test_illegal_device_type(monkeypatch):
    def mock_get(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={
                "deviceList": [
                    {
                        "deviceId": "ABCDE",
                        "deviceType": "Meter",
                        "hubDeviceId": "ABCDE",
                        "humidity": 50,
                        "temperature": 25.0,
                    }
                ]
            },
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_get)

    with pytest.raises(RuntimeError):
        client = SwitchBotAPIClient("token")
        Bot.create_by_id(client, "device_id")


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
        Light.create_by_id(client, "00-202001010000-12345678")


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
        Light.create_by_id(client, "00-202001010000-12345678")


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

    device = Light.create_by_id(client, "00-202001010000-12345678")
    result = device.turn_on()
    assert result.message == "success"

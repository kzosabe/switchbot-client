import pytest

from switchbot_client import ControlCommand, SwitchBotClient
from switchbot_client.api import SwitchBotAPIClient, SwitchBotAPIResponse
from switchbot_client.devices import AirConditioner, Bot, Light
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
        client = SwitchBotClient("token", "key")
        Bot(client, None)


def test_create_no_client():
    with pytest.raises(TypeError):
        Bot.create_by_id(client=None, device_id="id")


def test_create_no_device_id():
    with pytest.raises(TypeError):
        client = SwitchBotClient("token", "key")
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
        client = SwitchBotClient("token", "key")
        Bot.create_by_id(client, "device_id")

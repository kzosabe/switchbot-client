import pytest

from switchbot_client import ControlCommand, SwitchBotClient
from switchbot_client.api import SwitchBotAPIClient, SwitchBotAPIResponse
from switchbot_client.devices import (
    TV,
    AirConditioner,
    Fan,
    Light,
    PseudoRemoteDeviceStatus,
    SwitchBotRemoteDevice,
)
from switchbot_client.types import APIRemoteDeviceObject


def test_no_device(monkeypatch):
    def mock_devices(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={"infraredRemoteList": []},
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)

    with pytest.raises(RuntimeError):
        client = SwitchBotClient("token", "secret_key")
        Light.create_by_id(client, "00-202001010000-12345678")


def test_no_client(monkeypatch):
    def mock_devices(*args, **kwargs):
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={
                "infraredRemoteList": [
                    {
                        "deviceId": "00-202001010000-12345678",
                        "deviceName": "My TV",
                        "remoteType": "TV",
                        "hubDeviceId": "D12345678901",
                    },
                ]
            },
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)

    with pytest.raises(TypeError):
        TV.create_by_id(client=None, device_id="00-202001010000-12345678")


def test_illegal_device_type(monkeypatch):
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
        client = SwitchBotClient("token", "secret_key")
        Light.create_by_id(client, "00-202001010000-12345678")


def test_blank_hub_device_id(monkeypatch):
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
                        "hubDeviceId": "FFFFFFFFFFFF",
                    },
                ]
            },
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)

    client = SwitchBotClient("token", "secret_key")
    sut = AirConditioner.create_by_id(client, "00-202001010000-12345678")
    assert sut.hub_device_id is None


def test_validate_pseudo_status(monkeypatch):
    class Sut(SwitchBotRemoteDevice):
        def __init__(self, client: SwitchBotClient, device: APIRemoteDeviceObject):
            pseudo_status = PseudoRemoteDeviceStatus(
                device_id="00-202001010000-12345678",
                device_name="some not matched name",
                device_type="Air Conditioner",
                hub_device_id="FFFFFFFFFFFF",
                power=None,
                raw_data={},
            )
            super().__init__(client, device, pseudo_status)

    with pytest.raises(RuntimeError):
        Sut(
            SwitchBotClient("token", "secret_key"),
            {
                "deviceId": "00-202001010000-12345678",
                "deviceName": "My Air Conditioner",
                "remoteType": "Air Conditioner",
                "hubDeviceId": "FFFFFFFFFFFF",
            },
        )


def test_light(monkeypatch):
    client = SwitchBotClient("token", "secret_key")

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
        assert self == client.api_client
        assert device_id == "00-202001010000-12345678"
        assert command == ControlCommand.Common.TURN_ON
        assert parameter is None
        assert command_type is None
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={},
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices", mock_devices)
    monkeypatch.setattr(SwitchBotAPIClient, "devices_commands", mock_devices_commands)

    device_id = "00-202001010000-12345678"
    device = Light.create_by_id(client, device_id)

    assert device.status().device_id == device_id

    result = device.turn_on()
    assert result.message == "success"


def test_fan(monkeypatch):
    client = SwitchBotClient("token", "secret_key")

    def mock_devices_commands(
        self,
        device_id: str,
        command: str,
        parameter: str = None,
        command_type: str = None,
    ):
        assert self == client.api_client
        assert device_id == "00-202001010000-12345678"
        assert command == ControlCommand.Common.TURN_OFF
        assert parameter is None
        assert command_type is None
        return SwitchBotAPIResponse(
            status_code=100,
            message="success",
            body={},
        )

    monkeypatch.setattr(SwitchBotAPIClient, "devices_commands", mock_devices_commands)

    api_object = {
        "deviceId": "00-202001010000-12345678",
        "deviceName": "My Fan",
        "remoteType": "Fan",
        "hubDeviceId": "D12345678901",
    }
    device_id = "00-202001010000-12345678"
    device = Fan.create_by_api_object(client, api_object)

    assert device.status().device_id == device_id

    result = device.turn_off()
    assert result.message == "success"

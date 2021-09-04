import pytest
import requests
from switchbot_client.client import SwitchBotAPIClient


def test_init_no_token():
    with pytest.raises(RuntimeError):
        SwitchBotAPIClient()


def test_init_by_env(monkeypatch):
    monkeypatch.setenv("SWITCHBOT_OPEN_TOKEN", "abcdefg")
    sut = SwitchBotAPIClient()
    assert sut.token == "abcdefg"


def test_init_by_args():
    sut = SwitchBotAPIClient("123456")
    assert sut.token == "123456"


def test_init_with_domain():
    sut = SwitchBotAPIClient(
        token="foobar", api_host_domain="https://new-api.example.com"
    )
    assert sut.token == "foobar"
    assert sut.api_host_domain == "https://new-api.example.com"


def test_devices_status(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                "statusCode": 100,
                "message": "success",
                "body": {
                    "deviceId": "ABCDE",
                    "deviceType": "Meter",
                    "hubDeviceId": "ABCDE",
                    "humidity": 50,
                    "temperature": 25.0,
                },
            }

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")
    sut = client.devices_status("device_foo")

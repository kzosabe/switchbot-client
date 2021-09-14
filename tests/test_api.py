from unittest.mock import patch

import pytest
import requests

from switchbot_client.api import SwitchBotAPIClient
from switchbot_client.constants import AppConstants


@patch.object(SwitchBotAPIClient, "_load_config")
def test_init_no_token(patch_load_config):
    patch_load_config.return_value = None
    with pytest.raises(RuntimeError):
        SwitchBotAPIClient()


@patch.object(SwitchBotAPIClient, "_load_config")
def test_init_by_env(patch_load_config, monkeypatch):
    patch_load_config.return_value = None
    monkeypatch.setenv("SWITCHBOT_OPEN_TOKEN", "abcdefg")
    sut = SwitchBotAPIClient()
    assert sut.token == "abcdefg"


@patch("os.path.exists")
def test_init_by_config_file(patch_path_exists, mocker):
    m = mocker.patch("builtins.open", mocker.mock_open(read_data="token: foo"))
    patch_path_exists.return_value = True
    sut = SwitchBotAPIClient()
    m.assert_called_with(sut.config_file_path(), encoding="utf-8")


@patch("os.path.exists")
def test_init_by_config_file_no_token(patch_path_exists, mocker):
    m = mocker.patch("builtins.open", mocker.mock_open(read_data="not_token: foo"))
    patch_path_exists.return_value = True
    with pytest.raises(RuntimeError):
        SwitchBotAPIClient()


@patch("os.path.exists")
def test_init_by_config_file_no_file(patch_path_exists):
    patch_path_exists.return_value = False
    with pytest.raises(RuntimeError):
        SwitchBotAPIClient()


@patch.object(SwitchBotAPIClient, "_load_config")
def test_init_by_args(patch_load_config):
    patch_load_config.return_value = None
    sut = SwitchBotAPIClient("123456")
    assert sut.token == "123456"


@patch.object(SwitchBotAPIClient, "_load_config")
def test_init_with_domain(patch_load_config):
    patch_load_config.return_value = None
    sut = SwitchBotAPIClient(token="foobar", api_host_domain="https://new-api.example.com")
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
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")
    sut = client.devices_status("device_foo")

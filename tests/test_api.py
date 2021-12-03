from unittest.mock import patch

import pytest
import requests

from switchbot_client import ControlCommand
from switchbot_client.api import SwitchBotAPIClient
from switchbot_client.constants import AppConstants
from switchbot_client.devices import SwitchBotPhysicalDevice, SwitchBotRemoteDevice


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
def test_init_by_another_config_file(patch_path_exists, mocker):
    m = mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data="token: foo\napi_host_domain: https://new-api.example.com"),
    )
    patch_path_exists.return_value = True
    sut = SwitchBotAPIClient(config_file_path="~/.config/switch-bot-client/another-config.yml")
    m.assert_called_with("~/.config/switch-bot-client/another-config.yml", encoding="utf-8")
    assert sut.token == "foo"
    assert sut.api_host_domain == "https://new-api.example.com"


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


def test_devices(monkeypatch):
    expected = {
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

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_get(*args, **kwargs):
        return MockResponse()

    def dummy_method(self):
        pass

    monkeypatch.setattr(SwitchBotPhysicalDevice, "_check_device_type", dummy_method)
    monkeypatch.setattr(SwitchBotRemoteDevice, "_check_remote_type", dummy_method)
    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")
    sut = client.devices()
    assert sut.status_code == expected.get("statusCode")
    assert sut.message == expected.get("message")
    assert sut.body == expected.get("body")


def test_devices_status(monkeypatch):
    expected = {
        "statusCode": 100,
        "message": "success",
        "body": {
            "deviceId": "device_foo",
            "deviceType": "Meter",
            "hubDeviceId": "ABCDE",
            "humidity": 50,
            "temperature": 25.0,
        },
    }

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_get(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")
    sut = client.devices_status("device_foo")
    assert sut.status_code == expected.get("statusCode")
    assert sut.message == expected.get("message")
    assert sut.body == expected.get("body")


def test_devices_status_wrong_device_error(monkeypatch):
    expected = {
        "statusCode": 190,
        "message": "error message",
        "body": {},
    }

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_get(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")

    with pytest.raises(RuntimeError) as e:
        sut = client.devices_status("device_foo")
    assert "Wrong device ID or trying to get infrared virtual device status" in str(e.value)


def test_devices_status_broken_response(monkeypatch):
    expected = {
        "someInvalidResponse": "panic",
    }

    class MockResponse:
        def __init__(self):
            self.text = """{
                "someInvalidResponse": "panic",
            }"""

        @staticmethod
        def json():
            return expected

    def mock_get(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")

    with pytest.raises(RuntimeError) as e:
        sut = client.devices_status("device_foo")
    assert "format error" in str(e.value)


def test_devices_status_unauthorized(monkeypatch):
    expected = {
        "message": "Unauthorized",
    }

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_get(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")

    with pytest.raises(RuntimeError) as e:
        sut = client.devices_status("device_foo")
    assert "Http 401 Error. User permission is denied due to invalid token." in str(e.value)


def test_devices_commands(monkeypatch):
    expected = {
        "statusCode": 100,
        "message": "success",
        "body": {},
    }

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_post(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    client = SwitchBotAPIClient("token")
    sut = client.devices_commands(
        "device_foo",
        ControlCommand.ColorBulb.SET_BRIGHTNESS,
        parameter="50",
        command_type="command",
    )
    assert sut.status_code == expected.get("statusCode")
    assert sut.message == expected.get("message")
    assert sut.body == expected.get("body")


def test_scenes(monkeypatch):
    expected = {
        "statusCode": 100,
        "message": "success",
        "body": [
            {"sceneId": "S1", "sceneName": "Scene 1"},
            {"sceneId": "S2", "sceneName": "Scene 2"},
        ],
    }

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_get(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = SwitchBotAPIClient("token")
    sut = client.scenes()
    assert sut.status_code == expected.get("statusCode")
    assert sut.message == expected.get("message")
    assert sut.body == expected.get("body")


def test_scenes_execute(monkeypatch):
    expected = {
        "statusCode": 100,
        "message": "success",
        "body": {},
    }

    class MockResponse:
        @staticmethod
        def json():
            return expected

    def mock_post(*args, **kwargs):
        assert kwargs["headers"]["user-agent"] == f"switchbot-client/{AppConstants.VERSION}"
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    client = SwitchBotAPIClient("token")
    sut = client.scenes_execute(
        "scene_foo",
    )
    assert sut.status_code == expected.get("statusCode")
    assert sut.message == expected.get("message")
    assert sut.body == expected.get("body")

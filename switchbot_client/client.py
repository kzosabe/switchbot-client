from dataclasses import dataclass
import json
import os
import requests
import yaml


@dataclass
class SwitchBotAPIResponse:
    status_code: int
    message: str
    body: dict


class SwitchBotAPIClient:
    """
    https://github.com/OpenWonderLabs/SwitchBotAPI
    """

    DEFAULT_CONFIG_FILE_PATH = "~/.config/switchbot-client/config.yml"

    def __init__(
        self, token: str = None, api_host_domain: str = None, config_file_path: str = None
    ) -> None:
        if config_file_path is None:
            self.__config_file_path = config_file_path
        config = self._load_config()
        if token is not None:
            self.token = token
        elif "SWITCHBOT_OPEN_TOKEN" in os.environ and len(os.environ["SWITCHBOT_OPEN_TOKEN"]) > 0:
            self.token = os.environ["SWITCHBOT_OPEN_TOKEN"]
        elif config is not None and "token" in config.keys():
            self.token = config["token"]
        else:
            raise RuntimeError("no token specified")

        if api_host_domain is not None:
            self.api_host_domain = api_host_domain
        elif config is not None and "api_host_domain" in config.keys():
            self.api_host_domain = config["api_host_domain"]
        else:
            self.api_host_domain = "https://api.switch-bot.com"

    def devices(self) -> SwitchBotAPIResponse:
        response: requests.Response = requests.get(
            self._uri("v1.0/devices"), headers=self._headers()
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def devices_status(self, device_id: str) -> SwitchBotAPIResponse:
        response: requests.Response = requests.get(
            self._uri(f"v1.0/devices/{device_id}/status"), headers=self._headers()
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        if formatted_response.status_code == 190:
            raise RuntimeError(
                "Wrong device ID or trying to get infrared virtual device status",
                formatted_response,
            )
        return formatted_response

    def devices_commands(
        self,
        device_id: str,
        command: str,
        parameter: str = None,
        command_type: str = None,
    ) -> SwitchBotAPIResponse:
        payload = {
            "command": command,
        }

        if parameter is not None:
            payload["parameter"] = parameter
        if command_type is not None:
            payload["command_type"] = command_type
        response: requests.Response = requests.post(
            self._uri(f"v1.0/devices/{device_id}/commands"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def scenes(self) -> SwitchBotAPIResponse:
        response: requests.Response = requests.get(
            self._uri("v1.0/scenes"), headers=self._headers()
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def scenes_execute(self, scene_id: str) -> SwitchBotAPIResponse:
        response: requests.Response = requests.post(
            self._uri(f"v1.0/scenes/{scene_id}/execute"), headers=self._headers()
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def config_file_path(self):
        if self.__config_file_path is None:
            return os.path.expanduser(SwitchBotAPIClient.DEFAULT_CONFIG_FILE_PATH)
        return self.__config_file_path

    def _uri(self, endpoint: str):
        return f"{self.api_host_domain}/{endpoint}"

    def _headers(self):
        return {"content-type": "application/json", "authorization": self.token}

    def _load_config(self):
        config_file_path = self.config_file_path()
        if os.path.exists(config_file_path):
            with open(config_file_path, encoding="utf-8") as config_file:
                return yaml.safe_load(config_file)
        return None

    @staticmethod
    def _check_api_response(original_response: requests.Response):
        response = original_response.json()
        if "message" not in response:
            raise RuntimeError("format error")
        if response["message"] == "Unauthorized":
            raise RuntimeError(
                "Http 401 Error. User permission is denied due to invalid token.",
                original_response.text,
            )
        return SwitchBotAPIResponse(response["statusCode"], response["message"], response["body"])

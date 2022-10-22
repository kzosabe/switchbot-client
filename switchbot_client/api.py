import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import List

import requests
import yaml

from switchbot_client.constants import AppConstants


@dataclass
class SwitchBotAPIResponse:
    status_code: int
    message: str
    body: dict


class SwitchBotAPIClient:
    """
    A thin wrapper for SwitchBot API.
    It returns almost raw API response.
    https://github.com/OpenWonderLabs/SwitchBotAPI
    """

    DEFAULT_CONFIG_FILE_PATH = "~/.config/switchbot-client/config.yml"

    def __init__(
        self,
        token: str = None,
        secret_key: str = None,
        api_host_domain: str = None,
        config_file_path: str = None,
    ) -> None:
        self.__config_file_path = config_file_path
        self.api_version = "v1.1"
        config = self._load_config()

        if token is not None:
            self.token = token
        elif "SWITCHBOT_OPEN_TOKEN" in os.environ and len(os.environ["SWITCHBOT_OPEN_TOKEN"]) > 0:
            self.token = os.environ["SWITCHBOT_OPEN_TOKEN"]
        elif config is not None and "token" in config.keys():
            self.token = config["token"]
        else:
            raise RuntimeError("no token specified")

        if secret_key is not None:
            self.secret_key = secret_key
        elif "SWITCHBOT_SECRET_KEY" in os.environ and len(os.environ["SWITCHBOT_SECRET_KEY"]) > 0:
            self.secret_key = os.environ["SWITCHBOT_SECRET_KEY"]
        elif config is not None and "secret_key" in config.keys():
            self.secret_key = config["secret_key"]
        else:
            raise RuntimeError("no secret_key specified")

        if api_host_domain is not None:
            self.api_host_domain = api_host_domain
        elif config is not None and "api_host_domain" in config.keys():
            self.api_host_domain = config["api_host_domain"]
        else:
            self.api_host_domain = "https://api.switch-bot.com"

    def devices(self) -> SwitchBotAPIResponse:
        response: requests.Response = requests.get(self._uri("devices"), headers=self._headers())
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def devices_status(self, device_id: str) -> SwitchBotAPIResponse:
        response: requests.Response = requests.get(
            self._uri(f"devices/{device_id}/status"), headers=self._headers()
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
            self._uri(f"devices/{device_id}/commands"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def scenes(self) -> SwitchBotAPIResponse:
        response: requests.Response = requests.get(self._uri("scenes"), headers=self._headers())
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def scenes_execute(self, scene_id: str) -> SwitchBotAPIResponse:
        response: requests.Response = requests.post(
            self._uri(f"scenes/{scene_id}/execute"), headers=self._headers()
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def webhook_setup(self, url: str) -> SwitchBotAPIResponse:
        payload = {
            "action": "setupWebhook",
            "url": url,
            "deviceList": "ALL",
        }
        response: requests.Response = requests.post(
            self._uri("webhook/setupWebhook"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def webhook_query_url(self) -> SwitchBotAPIResponse:
        payload = {
            "action": "queryUrl",
        }
        response: requests.Response = requests.post(
            self._uri("webhook/queryWebhook"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def webhook_query_details(self, urls: List[str]) -> SwitchBotAPIResponse:
        payload = {"action": "queryDetails", "urls": urls}
        response: requests.Response = requests.post(
            self._uri("webhook/queryWebhook"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def webhook_update(self, config: dict) -> SwitchBotAPIResponse:
        payload = {"action": "updateWebhook", "config": config}
        response: requests.Response = requests.post(
            self._uri("webhook/updateWebhook"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def webhook_delete(self, url: str) -> SwitchBotAPIResponse:
        payload = {"action": "deleteWebhook", "url": url}
        response: requests.Response = requests.post(
            self._uri("webhook/deleteWebhook"),
            headers=self._headers(),
            data=json.dumps(payload),
        )
        formatted_response: SwitchBotAPIResponse = self._check_api_response(response)
        return formatted_response

    def config_file_path(self):
        if self.__config_file_path is None:
            return os.path.expanduser(SwitchBotAPIClient.DEFAULT_CONFIG_FILE_PATH)
        return self.__config_file_path

    def _uri(self, endpoint: str):
        return f"{self.api_host_domain}/{self.api_version}/{endpoint}"

    def _headers(self):
        version = AppConstants.VERSION
        return {
            "content-type": "application/json",
            "user-agent": f"switchbot-client/{version}",
            **self._generate_auth_header(),
        }

    def _generate_auth_header(self):
        nonce = ""
        timestamp = int(round(time.time() * 1000))
        string_to_sign = bytes(f"{self.token}{timestamp}{nonce}", "utf-8")
        secret = bytes(self.secret_key, "utf-8")
        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
        )
        return {
            "Authorization": self.token,
            "t": str(timestamp),
            "sign": str(sign, "utf-8"),
            "nonce": nonce,
        }

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
            raise RuntimeError("format error", original_response.text)
        if response["message"] == "Unauthorized":
            raise RuntimeError(
                "Http 401 Error. User permission is denied due to invalid token.",
                response,
            )
        return SwitchBotAPIResponse(response["statusCode"], response["message"], response["body"])

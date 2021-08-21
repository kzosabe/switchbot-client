import requests
import json
import os
from dataclasses import dataclass


@dataclass
class SwitchBotAPIResponse:
    status_code: int
    message: str
    body: dict


class SwitchBotAPIClient:
    """
    https://github.com/OpenWonderLabs/SwitchBotAPI
    """

    def __init__(self, token: str = None, api_host_domain: str = None) -> None:
        if token is not None:
            self.token = token
        elif (
            "SWITCHBOT_OPEN_TOKEN" in os.environ
            and len(os.environ["SWITCHBOT_OPEN_TOKEN"]) > 0
        ):
            self.token = os.environ["SWITCHBOT_OPEN_TOKEN"]
        else:
            raise RuntimeError("no token specified")

        self.api_host_domain = (
            "https://api.switch-bot.com" if api_host_domain is None else api_host_domain
        )

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

    def devices_control(
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

    def _uri(self, endpoint: str):
        return f"{self.api_host_domain}/{endpoint}"

    def _headers(self):
        return {"content-type": "application/json", "authorization": self.token}

    def _check_api_response(self, original_response: requests.Response):
        response = original_response.json()
        if not "message" in response:
            raise RuntimeError("format error")
        if response["message"] == "Unauthorized":
            raise RuntimeError(
                "Http 401 Error. User permission is denied due to invalid token.",
                original_response.text,
            )
        return SwitchBotAPIResponse(
            response["statusCode"], response["message"], response["body"]
        )

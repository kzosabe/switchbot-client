from typing import List

from switchbot_client.api import SwitchBotAPIClient
from switchbot_client.devices.base import SwitchBotDevice
from switchbot_client.devices.factory import SwitchBotDeviceFactory


class SwitchBotClient:
    """
    An abstract wrapper for SwitchBot API.
    It returns wrapped objects.
    """

    def __init__(
        self, token: str = None, api_host_domain: str = None, config_file_path: str = None
    ):
        self.client = SwitchBotAPIClient(token, api_host_domain, config_file_path)

    def devices(self) -> List[SwitchBotDevice]:
        response = self.client.devices().body
        devices = response["deviceList"]
        devices.extend(response["infraredRemoteList"])
        return [SwitchBotDeviceFactory.create(self.client, d) for d in devices]

from typing import List, Optional

from switchbot_client.api import SwitchBotAPIClient
from switchbot_client.devices.base import SwitchBotDevice
from switchbot_client.devices.factory import SwitchBotDeviceFactory
from switchbot_client.scenes import SwitchBotScene


class SwitchBotClient:
    """
    An abstract wrapper for SwitchBot API.
    It returns wrapped objects.
    """

    def __init__(
        self, token: str = None, api_host_domain: str = None, config_file_path: str = None
    ):
        self.api_client = SwitchBotAPIClient(token, api_host_domain, config_file_path)

    def devices(self) -> List[SwitchBotDevice]:
        response = self.api_client.devices().body
        devices = response["deviceList"]
        devices.extend(response["infraredRemoteList"])
        return [SwitchBotDeviceFactory.create(self, d) for d in devices]

    def device(self, device_id: str) -> Optional[SwitchBotDevice]:
        filtered = [d for d in self.devices() if d.device_id == device_id]
        if len(filtered) > 1:
            raise RuntimeError(f"duplicated device ids found: {filtered}")
        if len(filtered) == 0:
            return None
        return filtered[0]

    def scenes(self) -> List[SwitchBotScene]:
        response = self.api_client.scenes().body
        return [SwitchBotScene(self, scene["sceneId"], scene["sceneName"]) for scene in response]

    def scene(self, scene_id: str) -> Optional[SwitchBotScene]:
        filtered = [s for s in self.scenes() if s.scene_id == scene_id]
        if len(filtered) > 1:
            raise RuntimeError(f"duplicated scene ids found: {filtered}")
        if len(filtered) == 0:
            return None
        return filtered[0]

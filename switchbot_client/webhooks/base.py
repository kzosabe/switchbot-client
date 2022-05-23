from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass()
class SwitchBotWebhook:
    url: str
    enable: bool
    device_list: str
    create_time: datetime
    last_update_time: datetime

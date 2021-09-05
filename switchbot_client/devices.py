from switchbot_client import SwitchBotAPIClient, SwitchBotAPIResponse, ControlCommand


class SwitchBotDevice:
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        if client is None:
            raise TypeError
        self.client = client
        if device_id is None:
            raise TypeError
        self.device_id = device_id

    def check_device_type(self, expected_device_type: str):
        status = self.client.devices_status(self.device_id)
        actual_device_type = status.body["deviceType"]
        if actual_device_type != expected_device_type:
            raise RuntimeError(
                f"Illegal device type. "
                f"expected: {expected_device_type}, actual: {actual_device_type}"
            )

    def check_device_type_for_virtual_infrared(self, expected_device_type: str):
        infrared_remote_devices = self.client.devices().body["infraredRemoteList"]
        for device in infrared_remote_devices:
            if device["deviceId"] == self.device_id:
                actual_device_type = device["remoteType"]
                if actual_device_type == expected_device_type:
                    return
                raise RuntimeError(
                    f"Illegal device type. "
                    f"expected: {expected_device_type}, actual: {actual_device_type}"
                )
        raise RuntimeError(f"device not found: {self.device_id}")

    def status(self) -> SwitchBotAPIResponse:
        return self.client.devices_status(self.device_id)

    def control(
        self, command: str, parameter: str = None, command_type: str = None
    ) -> SwitchBotAPIResponse:
        return self.client.devices_control(self.device_id, command, parameter, command_type)


class Bot(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type("Bot")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.TURN_OFF)

    def press(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Bot.PRESS)


class Plug(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type("Plug")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Plug.TURN_OFF)


class Curtain(SwitchBotDevice):
    class Parameters:
        MODE_PERFORMANCE = "0"
        MODE_SILENT = "1"
        MODE_DEFAULT = "ff"

    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type("Curtain")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Curtain.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Curtain.TURN_OFF)

    def set_position(self, index: int, mode: str, position: int) -> SwitchBotAPIResponse:
        """
        mode(Parameters.MODE_XXX): 0 (Performance Mode), 1 (Silent Mode), ff (default mode)
        position: 0 ~ 100 (0 means opened, 100 means closed)
        """
        return self.control(
            ControlCommand.Curtain.SET_POSITION, parameter=f"{index},{mode},{position}"
        )


class Humidifier(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type("Humidifier")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Humidifier.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.Humidifier.TURN_OFF)

    def set_mode(self, mode: str) -> SwitchBotAPIResponse:
        """
        auto or 101 or 102 or 103 or {0~100}
        auto: set to Auto Mode
        101: set atomization efficiency to 34%
        102: set atomization efficiency to 67%
        103: set atomization efficiency to 100%
        """
        return self.control(ControlCommand.Humidifier.SET_MODE, parameter=mode)


class SmartFan(SwitchBotDevice):
    class Parameters:
        POWER_ON = "on"
        POWER_OFF = "off"
        FAN_MODE_STANDARD = 1
        FAN_MODE_NATURAL = 2

    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type("SmartFan")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.SmartFan.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.SmartFan.TURN_OFF)

    def set_all_status(
        self, power: str, fan_mode: int, fan_speed: int, shake_range: int
    ) -> SwitchBotAPIResponse:
        """
        power(Parameters.POWER_XXX): off, on
        fan_mode(Parameters.FAN_MODE_XXX): 1 (Standard), 2 (Natural)
        fan_speed: 1, 2, 3, 4
        shake_range: 0 ~ 120
        """
        return self.control(
            ControlCommand.SmartFan.SET_ALL_STATUS,
            parameter=f"{power},{fan_mode},{fan_speed},{shake_range}",
        )


class AirConditioner(SwitchBotDevice):
    class Parameters:
        MODE_AUTO = 1
        MODE_COOL = 2
        MODE_DRY = 3
        MODE_FAN = 4
        MODE_HEAT = 5
        FAN_SPEED_AUTO = 1
        FAN_SPEED_LOW = 2
        FAN_SPEED_MEDIUM = 3
        FAN_SPEED_HIGH = 4
        POWER_ON = "on"
        POWER_OFF = "off"

    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type_for_virtual_infrared("Air Conditioner")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.TURN_OFF)

    def set_all(
        self, temperature: int, mode: str, fan_speed: str, power: str
    ) -> SwitchBotAPIResponse:
        """
        temperature: temperature in celsius
        mode(Parameters.MODE_XXX): 1(auto), 2(cool), 3(dry), 4(fan), 5(heat)
        fan_speed(Parameters.FAN_SPEED_XXX): 1(auto), 2(low), 3(medium), 4(high);
        power(Parameters.POWER_XXX): on, off
        """
        return self.control(
            ControlCommand.VirtualInfrared.SET_ALL,
            parameter=f"{temperature},{mode},{fan_speed},{power}",
        )


class Light(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, device_id: str):
        super().__init__(client, device_id)
        self.check_device_type_for_virtual_infrared("Light")

    def turn_on(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.TURN_ON)

    def turn_off(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.TURN_OFF)

    def brightness_up(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.BRIGHTNESS_UP)

    def brightness_down(self) -> SwitchBotAPIResponse:
        return self.control(ControlCommand.VirtualInfrared.BRIGHTNESS_DOWN)

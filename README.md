# switchbot-client

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/switchbot-client.svg)](https://pypi.org/project/switchbot-client/)
[![PyPI - Library Version](https://img.shields.io/pypi/v/switchbot-client.svg)](https://pypi.org/project/switchbot-client/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/switchbot-client)](https://pypi.org/project/switchbot-client)
[![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-informational?style=flat-square)](README.md#License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An unofficial Python client implementation of the SwitchBot API.

## Table of Contents

- [Authentication](#authentication)
- [Usage](#usage)
- [License](#license)


## Authentication

Before you start using this client, you need to get an open token.
Please follow the instructions in the official documentation below.

https://github.com/OpenWonderLabs/SwitchBotAPI#authentication

Once you have the token, use one of the following methods to pass the information to the client.

### Environment variables

If the environment variable `SWITCHBOT_OPEN_TOKEN` is present, 
this client will automatically use this value.

```shell
export SWITCHBOT_OPEN_TOKEN=your_switchbot_open_token
python3 your_script.py
```

```python
# your_script.py
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
print(client.devices())
```

### Constructor Arguments

It is also possible to initialize the client by passing a token directly as an argument.

```python
from switchbot_client import SwitchBotAPIClient

your_token = "your_switchbot_open_token"
client = SwitchBotAPIClient(token=your_token)
print(client.devices())
```

### Config file

If `~/.config/switchbot-client/config.yml` exists and has a `token` entry, 
this client will automatically use the value.

```shell
mkdir -p ~/.config/switchbot-client
echo "token: your_switchbot_open_token" >>  ~/.config/switchbot-client/config.yml
python3 your_script.py
```

```python
# your_script.py
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
print(client.devices())
```

## Usage

### Get Device List

```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
result = client.devices()
print(result.body)
```

```
{'deviceList': [{'deviceId': 'ABCDEFG', 'deviceName': 'Meter 0A', 'deviceType': 'Meter', 'enableCloudService': True, 'hubDeviceId': 'ABCDE'}, {'deviceId': 'ABCDE', 'deviceName': 'Hub Mini 0', 'deviceType': 'Hub Mini', 'hubDeviceId': 'ABCDE'}], 'infraredRemoteList': [{'deviceId': '12345', 'deviceName': 'My Light', 'remoteType': 'Light', 'hubDeviceId': 'ABCDE'}, {'deviceId': '12345, 'deviceName': 'My Air Conditioner', 'remoteType': 'Air Conditioner', 'hubDeviceId': 'ABCDE'}]}
```

If you run the above code, you will get a list of all the devices associated with your SwitchBot account. 
You can perform operations on the acquired `deviceId`, such as manipulating it or getting its status.

### Get Device Status

```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
device_id = "YOUR_DEVICE_ID"
print(client.devices_status(device_id))
```

```
SwitchBotAPIResponse(status_code=100, message='success', body={'deviceId': 'ABCDE', 'deviceType': 'Meter', 'hubDeviceId': 'ABCDE', 'humidity': 50, 'temperature': 25.0})
```

This function allows you to get the status of a device.
Note that only physical devices can be targeted, not virtual infrared remote devices.

Please refer to the following official document to know what kind of information can be obtained from each device.

https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-status

### Control Device

```python
from switchbot_client import SwitchBotAPIClient, ControlCommand

client = SwitchBotAPIClient()
device_id = "12345" # My Light(virtual infrared remote devices)
print(client.devices_commands(device_id, ControlCommand.VirtualInfrared.TURN_ON))
```

```
SwitchBotAPIResponse(status_code=100, message='success', body={})
```

It allows you to control the specified device.
The `ControlCommand` class and the following documents define the commands that can be executed.

https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands

### Get Scene List

```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
print(client.scenes())
```

```
SwitchBotAPIResponse(status_code=100, message='success', body=[{'sceneId': '12345', 'sceneName': 'My Scene'}])
```

You can get a list of all the scenes associated with your SwitchBot account.
Note that only manual scenes are returned from this api.

### Execute Scene
```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
print(client.scenes_execute("12345"))
```

```
SwitchBotAPIResponse(status_code=100, message='success', body={})
```
The specified scene can be executed immediately.

### Object interface

Devices can be manipulated via an easy-to-use object wrapped API.

```python
from switchbot_client import SwitchBotAPIClient
from switchbot_client.devices import Light, AirConditioner

client = SwitchBotAPIClient()

# You can get your Lights and Air Conditioners device ids by
# print(client.devices().body["infraredRemoteList"])

light = Light(client, device_id="my_light_device_id")
light.turn_on()

air_conditioner = AirConditioner(client, device_id="my_air_conditioner_device_id")
air_conditioner.set_all(
    temperature=25,
    mode=AirConditioner.Parameters.MODE_DRY,
    fan_speed=AirConditioner.Parameters.FAN_SPEED_AUTO,
    power=AirConditioner.Parameters.POWER_ON
)
```

### Examples

```python
from switchbot_client.enums import ControlCommand
from switchbot_client import SwitchBotAPIClient


def control_all_infrared_remotes_by_type(type: str, command: str):
    client = SwitchBotAPIClient()
    devices = client.devices()
    infrared_remotes = devices.body["infraredRemoteList"]
    devices = filter(lambda d: d["remoteType"] == type, infrared_remotes)

    for d in devices:
        client.devices_commands(d["deviceId"], command)


def call_this_function_when_i_go_out():
    print("turn off all lights and air conditioners...")
    control_all_infrared_remotes_by_type(
        "Light", ControlCommand.VirtualInfrared.TURN_OFF
    )
    control_all_infrared_remotes_by_type(
        "Air Conditioner", ControlCommand.VirtualInfrared.TURN_OFF
    )
    print("done")
```

## License

Licensed under either of

- Apache License, Version 2.0
   ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license
   ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.

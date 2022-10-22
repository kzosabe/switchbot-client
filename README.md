# switchbot-client

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/switchbot-client.svg)](https://pypi.org/project/switchbot-client/)
[![PyPI - Library Version](https://img.shields.io/pypi/v/switchbot-client.svg)](https://pypi.org/project/switchbot-client/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/switchbot-client)](https://pypi.org/project/switchbot-client)
[![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-informational?style=flat-square)](README.md#License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An unofficial Python client implementation of the SwitchBot API.

## About this version

switchbot-client-0.x.x is the implementation for [SwitchBot API version 1.0](https://github.com/OpenWonderLabs/SwitchBotAPI/blob/main/README-v1.0.md).
The implementation for API version 1.1 or later will proceed with switchbot-client-1.x.x.
Please select the library version according to the API version you use.
Development of switchbot-client-0.x.x will likely cease with the SwitchBot API version update, and we recommend moving to 1.x.x.

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
python your_script.py
```

```python
# your_script.py
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
print(client.devices())
```

### Constructor Arguments

It is also possible to initialize the client by passing a token directly as an argument.

```python
from switchbot_client import SwitchBotClient

your_token = "your_switchbot_open_token"
client = SwitchBotClient(token=your_token)
print(client.devices())
```

### Config file

If `~/.config/switchbot-client/config.yml` exists and has a `token` entry, 
this client will automatically use the value.

```shell
mkdir -p ~/.config/switchbot-client
echo "token: your_switchbot_open_token" >>  ~/.config/switchbot-client/config.yml
python your_script.py
```

```python
# your_script.py
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
print(client.devices())
```

## Usage

### Get Device List

```python
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
result = client.devices()
print(result)
```

```
[Meter({'device_id': 'ABCDEFG', 'device_type': 'Meter', 'device_name': 'Meter 0A', 'hub_device_id': 'ABCDE', 'is_virtual_infrared': False}), HubMini({'device_id': 'ABCDEFG', 'device_type': 'Hub Mini', 'device_name': 'Hub Mini 0', 'hub_device_id': None, 'is_virtual_infrared': False}), Light({'device_id': '12345', 'device_type': 'Light', 'device_name': 'My Light', 'hub_device_id': 'ABCDE', 'is_virtual_infrared': True}), AirConditioner({'device_id': '12345', 'device_type': 'Air Conditioner', 'device_name': 'My Air Conditioner', 'hub_device_id': 'ABCDE', 'is_virtual_infrared': True})]
```

If you run the above code, you will get a list of all the devices associated with your SwitchBot account. 
You can perform operations on the acquired `device_id`, such as manipulating it or getting its status.

### Get Device Status

```python
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
device_id = "YOUR_DEVICE_ID"
print(client.device(device_id).status())
```

```
DeviceStatus(device_id='ABCDE', device_type='Meter', device_name='Meter 0', hub_device_id='ABCDE', data={'deviceId': 'ABCDE', 'deviceType': 'Meter', 'hubDeviceId': 'ABCDE', 'humidity': 50, 'temperature': 25.0})
```

This function allows you to get the status of a device.
Note that only the physical device returns accurate results, while the virtual infrared remote device is inaccurate, 
storing the results of the most recent operation.

Please refer to the following official document to know what kind of information can be obtained from each device.

https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-status

### Control Device

```python
from switchbot_client import SwitchBotClient
from switchbot_client.devices import Light

client = SwitchBotClient()
device_id = "12345"  # My Light(virtual infrared remote devices)
device = Light.create_by_id(client, device_id)
print(device.turn_on())
```

```
SwitchBotCommandResult(status_code=100, message='success', response_body={})
```

It allows you to control the specified device.
The following documents define the commands that can be executed.

https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands

### Get Scene List

```python
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
print(client.scenes())
```

```
[SwitchBotScene({'scene_id': '12345', 'scene_name': 'My Scene1'}), SwitchBotScene({'scene_id': '23456', 'scene_name': 'My Scene2'})]
```

You can get a list of all the scenes associated with your SwitchBot account.
Note that only manual scenes are returned from this api.

### Execute Scene
```python
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
print(client.scene("12345").execute())
```

```
SwitchBotCommandResult(status_code=100, message='success', response_body={})
```
The specified scene can be executed immediately.

### Webhooks

```python
from switchbot_client import SwitchBotClient

client = SwitchBotClient()
client.set_webhook(url="https://example.com/foo", enable=True)
print(client.webhooks())
```

```
[SwitchBotWebhook(url='https://example.com/foo', enable=True, device_list='ALL', create_time=datetime.datetime(2022, 1, 1, 12, 0, 0, 123456), last_update_time=datetime.datetime(2022, 1, 1, 12, 0, 0, 123456))]
```

You can handle [webhook](https://github.com/OpenWonderLabs/SwitchBotAPI#webhook) configurations via SwitchBotClient.

### Raw API interface

Devices and scenes also can be manipulated via the low-level raw API client.
The `SwitchBotAPIClient` class has methods for each endpoints of SwitchBot API.

For example the `/v1.0/devices` endpoint is implemented as `SwitchBotAPIClient.devices()`, 
the `/v1.0/devices/{device_id}/status"` endpoint is implemented as `SwitchBotAPIClient.devices_status(device_id: str)`.


### Examples

```python
from switchbot_client import devices
from switchbot_client import SwitchBotClient


def call_this_function_when_i_go_out():
    client = SwitchBotClient()
    print("turn off all lights and air conditioners...")
    for d in client.devices():
        if isinstance(d, devices.Light):
            d.turn_off()

        if isinstance(d, devices.ColorBulb):
            d.turn_off()

        if isinstance(d, devices.AirConditioner):
            d.turn_off()
    print("done")


def control_devices_by_temperature():
    client = SwitchBotClient()
    all_devices = client.devices()

    temperatures = [d.temperature() for d in all_devices if isinstance(d, devices.Meter)]
    temperature = min(temperatures)

    color_bulbs = [d for d in all_devices if isinstance(d, devices.ColorBulb)]
    air_conditioners = [d for d in all_devices if isinstance(d, devices.AirConditioner)]

    if temperature > 25.0:
        print("hot!")
        for d in color_bulbs:
            d.set_color("#FF0000")

        for d in air_conditioners:
            d.set_all(
                temperature=20.0,
                mode=devices.AirConditioner.Parameters.MODE_COOL,
                fan_speed=devices.AirConditioner.Parameters.FAN_SPEED_HIGH,
                power=devices.AirConditioner.Parameters.POWER_ON
            )

    elif temperature < 15.0:
        print("cold!")
        for d in color_bulbs:
            d.set_color("#0000FF")

        for d in air_conditioners:
            d.set_all(
                temperature=20.0,
                mode=devices.AirConditioner.Parameters.MODE_HEAT,
                fan_speed=devices.AirConditioner.Parameters.FAN_SPEED_HIGH,
                power=devices.AirConditioner.Parameters.POWER_ON
            )
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

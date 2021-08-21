# switchbot-client

[![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-informational?style=flat-square)](README.md#License)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/switchbot-client.svg)](https://pypi.org/project/switchbot-client/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/switchbot-client)](https://pypi.org/project/switchbot-client)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Table of Contents

- [Authentication](#authentication)
- [Usage](#usage)
- [Examples](#examples)
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
export SWITCHBOT_OPEN_TOKEN=yourswitchbotopentoken
python3 your_script_using_switchbot_client.py
```

```python
# your_script_using_switchbot_client.py
client = SwitchBotAPIClient()
result = client.devices()
```

### Constructor Arguments

It is also possible to initialize the client by passing a token directly as an argument.

```python
from switchbot_client import SwitchBotAPIClient

your_token = "yourswitchbotopentoken"
client = SwitchBotAPIClient(token=your_token)
result = client.devices()
```


## Usage

### Get Device List

```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
result = client.devices()
print(result.body)
```

=>
```
{'deviceList': [{'deviceId': 'ABCDEFG', 'deviceName': 'Meter 0A', 'deviceType': 'Meter', 'enableCloudService': True, 'hubDeviceId': 'ABCDE'}, {'deviceId': 'ABCDE', 'deviceName': 'Hub Mini 0', 'deviceType': 'Hub Mini', 'hubDeviceId': 'ABCDE'}], 'infraredRemoteList': [{'deviceId': '12345', 'deviceName': 'My Light', 'remoteType': 'Light', 'hubDeviceId': 'ABCDE'}, {'deviceId': '12345, 'deviceName': 'My Air Conditioner', 'remoteType': 'Air Conditioner', 'hubDeviceId': 'ABCDE'}]}
```

If you run the above code, you will get a list of all the devices associated with your SwitchBot account. 
You can perform operations on the acquired `deviceId`, such as manipulating it or getting its status.

### Get Device Status

```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
device_id = "YOURDEVICEID"
print(client.devices_status(device_id))
```
=>
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
print(client.devices_control(device_id, ControlCommand.VirtualInfrared.TURN_ON))
```
=>
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
=>
```
SwitchBotAPIResponse(status_code=100, message='success', body=[{'sceneId': '12345', 'sceneName': 'My Scene'}])
```

You can get a list of all the scenes associated with your SwitchBot account.

### Execute Scene
```python
from switchbot_client import SwitchBotAPIClient

client = SwitchBotAPIClient()
print(client.scenes_execute("12345"))
```
=>
```
SwitchBotAPIResponse(status_code=100, message='success', body={})
```
The specified scene can be executed immediately.


## License

Licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

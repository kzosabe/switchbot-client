0.4.0, 2022-05-24
-------------------------

- Add webhook support(#77, #78)
  - You can create, get, set, and delete webhook configurations via SwitchBotClient or SwitchBotAPIClient
- Add pseudo status for AirConditioner(#59)
- Fix Humidifier behavior when lackWater column is missing(#58)

0.3.2, 2022-02-03
-------------------------

- Add new devices
  - Plug Mini, Strip Light, Meter Plus, Lock
- Add pseudo status for remote devices
  - Now you can call status() on remote devices
  - It returns the value specified in the last change operation, 
    which may or may not match the true state of the device

0.3.1, 2021-11-27
-------------------------

- Bug fix
  - Fix import issue when using physical device objects

0.3.0, 2021-11-27
-------------------------

- API Interface Change
  - Use SwitchBotClient instead of SwitchBotAPIClient in all public method arguments
- Add control and status methods for each device classes

0.2.0, 2021-10-30
-------------------------

- API Interface Change
  - Use object interface as the main one
  - It is recommended to use SwitchBotClient instead of SwitchBotAPIClient
- Add new devices(Motion Sensor, Contact Sensor, Color Bulb, Remote)
- Use `switchbot-client/{version}` as the user agent when requesting the SwitchBot API
- Remove Python 3.6.x support and add Python 3.10.x support

0.1.2, 2021-09-11
-------------------------

- Support ~/.config/switchbot-client config file
- Add object interface for all devices
- Rename devices_control to devices_commands

0.1.1, 2021-09-05
-------------------------

- Add object interface

0.1.0, 2021-09-04
-------------------------

- Add basic implementation

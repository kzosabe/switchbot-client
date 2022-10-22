class DeviceType:
    HUB = "Hub"
    HUB_PLUS = "Hub Plus"
    HUB_MINI = "Hub Mini"
    BOT = "Bot"
    CURTAIN = "Curtain"
    PLUG = "Plug"
    PLUG_MINI_US = "Plug Mini (US)"
    PLUG_MINI_JP = "Plug Mini (JP)"
    METER = "Meter"
    METER_PLUS_US = "Meter Plus (US)"
    METER_PLUS_JP = "Meter Plus (JP)"
    MOTION_SENSOR = "Motion Sensor"
    CONTACT_SENSOR = "Contact Sensor"
    COLOR_BULB = "Color Bulb"
    HUMIDIFIER = "Humidifier"
    SMART_FAN = "Smart Fan"
    STRIP_LIGHT = "Strip Light"
    INDOOR_CAM = "Indoor Cam"
    REMOTE = "Remote"  # undocumented in official api reference?
    LOCK = "Lock"
    ROBOT_VACUUM_CLEANER_S1_PLUS = "Robot Vacuum Cleaner S1"
    ROBOT_VACUUM_CLEANER_S1 = "Robot Vacuum Cleaner S1 Plus"


class RemoteType:
    AIR_CONDITIONER = "Air Conditioner"
    TV = "TV"
    LIGHT = "Light"
    IPTV_STREAMER = "IPTV/Streamer"
    SET_TOP_BOX = "Set Top Box"
    DVD = "DVD"
    FAN = "Fan"
    PROJECTOR = "Projector"
    CAMERA = "Camera"
    AIR_PURIFIER = "Air Purifier"
    SPEAKER = "Speaker"
    WATER_HEATER = "Water Heater"
    VACUUM_CLEANER = "Vacuum Cleaner"
    OTHERS = "Others"


class ControlCommand:
    class Common:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"

    class Bot:
        PRESS = "press"

    class PlugMiniUs:
        TOGGLE = "toggle"

    class PlugMiniJp:
        TOGGLE = "toggle"

    class Curtain:
        SET_POSITION = "setPosition"

    class Humidifier:
        SET_MODE = "setMode"

    class ColorBulb:
        TOGGLE = "toggle"
        SET_BRIGHTNESS = "setBrightness"
        SET_COLOR = "setColor"
        SET_COLOR_TEMPERATURE = "setColorTemperature"

    class SmartFan:
        SET_ALL_STATUS = "setAllStatus"

    class StripLight:
        TOGGLE = "toggle"
        SET_BRIGHTNESS = "setBrightness"
        SET_COLOR = "setColor"

    class RobotVacuumCleaner:
        START = "start"
        STOP = "stop"
        DOCK = "dock"
        POW_LEVEL = "PowLevel"

    class VirtualInfrared:
        SET_ALL = "setAll"
        SET_CHANNEL = "SetChannel"
        VOLUME_ADD = "volumeAdd"
        VOLUME_SUB = "volumeSub"
        CHANNEL_ADD = "channelAdd"
        CHANNEL_SUB = "channelSub"
        SET_MUTE = "setMute"
        FAST_FORWARD = "FastForward"
        REWIND = "Rewind"
        NEXT = "Next"
        PREVIOUS = "Previous"
        PAUSE = "Pause"
        PLAY = "Play"
        STOP = "Stop"
        SWING = "swing"
        TIMER = "timer"
        LOW_SPEED = "lowSpeed"
        MIDDLE_SPEED = "middleSpeed"
        HIGH_SPEED = "highSpeed"
        BRIGHTNESS_UP = "brightnessUp"
        BRIGHTNESS_DOWN = "brightnessDown"

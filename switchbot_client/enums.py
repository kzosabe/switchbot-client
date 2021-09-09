class DeviceType:
    HUB = "Hub"
    HUB_PLUS = "Hub Plus"
    HUB_MINI = "Hub Mini"
    BOT = "Bot"
    CURTAIN = "Curtain"
    PLUG = "Plug"
    METER = "Meter"
    HUMIDIFIER = "Humidifier"
    SMART_FAN = "Smart Fan"
    INDOOR_CAM = "Indoor Cam"


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
    class Bot:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"
        PRESS = "press"

    class Plug:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"

    class Curtain:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"
        SET_POSITION = "setPosition"

    class Humidifier:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"
        SET_MODE = "setMode"

    class SmartFan:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"
        SET_ALL_STATUS = "setAllStatus"

    class VirtualInfrared:
        TURN_ON = "turnOn"
        TURN_OFF = "turnOff"
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

from enum import Enum


# Enumeration classes for voice assistant configurations
class Sex(Enum):
    Man = 1
    Woman = 2


class Languages(Enum):
    RU = 3
    EN = 4


class Commands(Enum):
    failure = 0
    greeting = 1
    farewell = 2
    google_search = 3
    run_application = 4
    volume_settings = 5
    screen_brightness_settings = 6
    create_promt = 7


class VolumeCommands(Enum):
    failure = 0
    mute = 1
    unmute = 2
    set_value = 3
    up = 4
    down = 5


class ScreenBrightnessCommands(Enum):
    failure = 0
    set_value = 1
    up = 2
    down = 3

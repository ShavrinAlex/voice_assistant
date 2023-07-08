from enum import Enum, IntEnum


# Enumeration classes for voice assistant configurations
class Sex(Enum):
    Man = 1
    Woman = 2


class Languages(Enum):
    RU = 3
    EN = 4


class GeneralCommands(Enum):
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


class DateCommands(IntEnum):
    Monday = 20
    Tuesday = 21
    Wednesday = 22
    Thursday = 23
    Friday = 24
    Saturday = 25
    Sunday = 26
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12
    Today = 13
    Tomorrow = 14
    AfterTomorrow = 15
    

class AppOpenerCommands(Enum):
    failure = 0
    open = 1
    close = 2
    nonrequest = 3
    request = 4

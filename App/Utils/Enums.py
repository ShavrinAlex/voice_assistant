from enum import Enum


# Enumeration classes for voice assistant configurations
class Sex(Enum):
    Man = 1
    Woman = 2


class Languages(Enum):
    RU = 3
    EN = 4


class Command(Enum):
    failure = 0
    greeting = 1
    farewell = 2
    google_search = 3
    run_application = 4

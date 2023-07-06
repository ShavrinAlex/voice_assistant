import screen_brightness_control as sbc
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Enums import ScreenBrightnessCommands


COMMANDS_FILE = 'App/ScreenBrightnessController/Commands.json'
INDEX_OF_PROBABILITY = 0.4


class ScreenBrightnessController:
    """
    Класс контроллера яркости экрана
    Screen Brightness Controller class
    """

    def __init__(self, display_index=0, bright_delta=10) -> None:
        self.__display_index = display_index
        self.__bright_delta = bright_delta
        self.__cmd_recognizer = CommandRecognizer(ScreenBrightnessCommands, COMMANDS_FILE, INDEX_OF_PROBABILITY)

    def get_brightness(self) -> list[int]:
        return sbc.get_brightness()

    def __get_bright_value(self, command_string: str) -> int:
        try:
            return int(''.join(filter(str.isdigit, command_string)))
        except ValueError:
            return self.get_brightness()[self.__display_index]

    def set_brightness(self, brightness: int) -> None:
        if brightness < 0 or brightness > 100:
            print('Incorrect brightness value')
            return

        sbc.set_brightness(brightness)

    def execute(self, command_string: str) -> None:
        command = self.__cmd_recognizer.get_command(command_string)
        if command == ScreenBrightnessCommands.set_value:
            bright_value = self.__get_bright_value(command_string)
            self.set_brightness(bright_value)
        elif command == ScreenBrightnessCommands.up:
            current_brightness = self.get_brightness()[self.__display_index]
            bright_value = self.__get_bright_value(command_string)
            if bright_value != current_brightness:
                self.set_brightness(min(100, current_brightness + bright_value))
            else:
                self.set_brightness(min(100, current_brightness + self.__bright_delta))
        elif command == ScreenBrightnessCommands.down:
            current_brightness = self.get_brightness()[self.__display_index]
            bright_value = self.__get_bright_value(command_string)
            if bright_value != current_brightness:
                self.set_brightness(max(0, current_brightness - bright_value))
            else:
                self.set_brightness(max(0, current_brightness - self.__bright_delta))
        elif command == ScreenBrightnessCommands.failure:
            print('Incorrect command')

'''
def main():
    SCBC = ScreenBrightnessController()
    while True:
        # Ввод процентного значения яркости от пользователя
        command = input("Введите команду: ")

        # Установка громкости
        SCBC.execute(command)
        print(SCBC.get_brightness())


if __name__ == "__main__":
    main()
'''

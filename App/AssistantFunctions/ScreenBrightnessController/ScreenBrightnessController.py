import screen_brightness_control as sbc
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Enums import ScreenBrightnessCommands
from App.VoiceAssistant import VoiceAssistant


COMMANDS_FILE = 'App/AssistantFunctions/ScreenBrightnessController/Commands.json'
INDEX_OF_PROBABILITY = 0.4


class ScreenBrightnessController:
    """
    Класс контроллера яркости экрана
    Screen Brightness Controller class
    """

    def __init__(self, mediator: VoiceAssistant, display_index=0, bright_delta=10) -> None:
        self.__mediator = mediator
        self.__display_index = display_index
        self.__bright_delta = bright_delta
        self.__cmd_recognizer = CommandRecognizer(ScreenBrightnessCommands, COMMANDS_FILE, INDEX_OF_PROBABILITY)

    def get_brightness(self) -> list[int]:
        return sbc.get_brightness()

    def __get_bright_value(self, command_string: str) -> int:
        try:
            return int(''.join(filter(str.isdigit, command_string)))
        except ValueError:
            return -1

    def set_brightness(self, brightness: int) -> None:
        sbc.set_brightness(brightness)

    def execute(self, command_string: str) -> None:
        command = self.__cmd_recognizer.get_command(command_string)
        if command == ScreenBrightnessCommands.set_value:
            bright_value = self.__get_bright_value(command_string)
            if 0 <= bright_value <= 100:
                self.set_brightness(bright_value)
                self.__mediator.reproduce_speech(f"Яркость экрана {bright_value}")
            else:
                self.__mediator.reproduce_speech("Некорректное значение яркости, повторите еще раз")

        elif command == ScreenBrightnessCommands.up:
            current_brightness = self.get_brightness()[self.__display_index]
            delta_bright_value = self.__get_bright_value(command_string)
            if delta_bright_value == -1:
                delta_bright_value = self.__bright_delta
            new_bright_value = min(100, current_brightness + delta_bright_value)
            if new_bright_value == 100:
                self.__mediator.reproduce_speech(f"Яркость экрана будет повышена до ста")
            self.set_brightness(new_bright_value)
            if new_bright_value != 100:
                self.__mediator.reproduce_speech(f"Яркость экрана повышена на {delta_bright_value}")

        elif command == ScreenBrightnessCommands.down:
            current_brightness = self.get_brightness()[self.__display_index]
            delta_bright_value = self.__get_bright_value(command_string)
            if delta_bright_value == -1:
                delta_bright_value = self.__bright_delta
            new_bright_value = max(0, current_brightness - delta_bright_value)
            if new_bright_value == 0:
                self.__mediator.reproduce_speech(f"Яркость экрана будет понижена до нуля")
            self.set_brightness(new_bright_value)
            if new_bright_value != 0:
                self.__mediator.reproduce_speech(f"Яркость экрана понижена на {delta_bright_value}")

        elif command == ScreenBrightnessCommands.failure:
            self.__mediator.reproduce_speech("К сожалению, я не понимаю такой команды настройки яркости")

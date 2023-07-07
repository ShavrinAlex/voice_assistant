from App.VoiceAssistant import VoiceAssistant
from App.Utils.Enums import GeneralCommands

# Import modules
from App.AssistantFunctions.GoogleSearcher.GoogleSearcher import GoogleSearcher
from App.AssistantFunctions.Reminder.Reminder import Reminder
from App.AssistantFunctions.AppOpener.OpenApp import OpenApp
from App.AssistantFunctions.SoundController.SoundController import SoundController
from App.AssistantFunctions.ScreenBrightnessController.ScreenBrightnessController import ScreenBrightnessController


class CommandsSwitcher:
    """
    Класс, осуществляющий выполнение комманды, соответствующей запросу пользователя
    The class that executes the command corresponding to the user's request
    """

    def __init__(self, mediator: VoiceAssistant) -> None:
        self.__mediator = mediator
        self.__google_search = GoogleSearcher(self.__mediator)
        self.__openApp = OpenApp()
        self.__reminder = Reminder(self.__mediator)
        self.__sound_controller = SoundController()
        self.__brightness_controller = ScreenBrightnessController()
        
    def switch(self, command: GeneralCommands, command_text: str) -> None:
        """
        Функция, непосредственно осуществляющая переключение
        Switching function directly

        :param command: GeneralCommands - комманда голосовому ассистенту
        :param command_text: string - строковой вид запроса пользователя

        :param command: GeneralCommands - command to the voice assistant
        :param command_text: string - string form of the user's request
        """

        if command == GeneralCommands.google_search:
            self.__google_search.search()
        elif command == GeneralCommands.run_application:
            self.__openApp.open_app(command_text)
        elif command == GeneralCommands.create_promt:
            self.__reminder.create_promt()
        elif command == GeneralCommands.greeting:
            self.__mediator.reproduce_greetings()
        elif command == GeneralCommands.farewell:
            self.__mediator.reproduce_farewell_and_quit()
        elif command == GeneralCommands.volume_settings:
            self.__sound_controller.execute(command_text)
        elif command == GeneralCommands.screen_brightness_settings:
            self.__brightness_controller.execute(command_text)
        elif command == GeneralCommands.failure:
            self.__mediator.reproduce_failure_phrase()

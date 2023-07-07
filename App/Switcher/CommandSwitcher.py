from App.VoiceAssistant import VoiceAssistant
from App.Utils.Enums import GeneralCommands

# Import modules
from App.AssistantFunctions.Google.GoogleSearch import GoogleSearch
from App.AssistantFunctions.Reminder.Reminder import Reminder
from App.AssistantFunctions.AppOpener.OpenApp import OpenApp
from App.AssistantFunctions.SoundController.SoundController import SoundController
from App.AssistantFunctions.ScreenBrightnessController.ScreenBrightnessController import ScreenBrightnessController


class Switcher:
    def __init__(self, mediator: VoiceAssistant):
        self.__mediator = mediator
        self.__google_search = None
        self.__openApp = None
        self.__reminder = None
        self.__sound_controller = None
        self.__brightness_controller = None
        
    def switch(self, command: GeneralCommands, command_text: str):
        if command == GeneralCommands.google_search:
            return self.search_google()
        elif command == GeneralCommands.run_application:
            return self.open_app(command_text)
        elif command == GeneralCommands.create_promt:
            return self.create_promt()
        elif command == GeneralCommands.greeting:
            return self.__mediator.reproduce_greetings()
        elif command == GeneralCommands.farewell:
            return self.__mediator.reproduce_farewell_and_quit()
        elif command == GeneralCommands.volume_settings:
            if self.__sound_controller is None:
                self.__sound_controller = SoundController()
            self.__sound_controller.execute(command_text)
        elif command == GeneralCommands.screen_brightness_settings:
            if self.__brightness_controller is None:
                self.__brightness_controller = ScreenBrightnessController()
            self.__brightness_controller.execute(command_text)
    
    def search_google(self):
        if self.__google_search is None:
            self.__google_search = GoogleSearch(self.__mediator)
        self.__google_search.search()
    
    def open_app(self, request):
        if self.__openApp is None:
            self.__openApp = OpenApp()
        self.__openApp.open_app(request)

    def create_promt(self):
        if self.__reminder is None:
            self.__reminder = Reminder(self.__mediator)
        self.__reminder.create_promt()

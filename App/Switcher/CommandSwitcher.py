from App.VoiceAssistant import VoiceAssistant
from App.Utils.Enums import Commands

# Import modules
from App.AssistantFunctions.Google.GoogleSearch import GoogleSearch
from App.AssistantFunctions.Reminder.Reminder import Reminder
from App.AssistantFunctions.AppOpener.OpenApp import OpenApp
from App.SoundController.SoundController import SoundController
from App.ScreenBrightnessController.ScreenBrightnessController import ScreenBrightnessController

class Switcher:
    def __init__(self, mediator: VoiceAssistant):
        self.__mediator = mediator
        self.__google_search = None
        self.__openApp = None
        self.__reminder = None
        
    def switch(self, command: Commands, command_text: str):
        if command == Commands.google_search:
            return self.search_google()
        elif command == Commands.run_application:
            return self.open_app(command_text)
        elif command == Commands.create_promt:
            return self.create_promt()
        elif command == Commands.greeting:
            return self.__mediator.reproduce_greetings()
        elif command == Commands.farewell:
            return self.__mediator.reproduce_farewell_and_quit()
        elif (command == Commands.volume_settings):
            sc = SoundController()
            sc.execute(self.__speech_string)
        elif (command == Commands.screen_brightness_settings):
            sbc = ScreenBrightnessController()
            sbc.execute(self.__speech_string)
    
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

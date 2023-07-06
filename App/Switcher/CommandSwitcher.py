from App.VoiceAssistant import VoiceAssistant
from App.Utils.Enums import Command
from App.AssistantFunctions.Google.GoogleSearch import GoogleSearch

class Switcher:
    def __init__(self, mediator: VoiceAssistant):
        self.__mediator = mediator
        self.__google_search = None
        self.__openApp = None
        
    def switch(self,command):
        if command == Command.google_search:
            return self.searchGoogle()
        elif command == Command.run_application:
            return self.openApp()
    
    def searchGoogle(self):
        if self.__google_search is None:
            self.__google_search = GoogleSearch(self.__mediator)
        self.__google_search.search()
    
    def openApp(self):
        pass
        
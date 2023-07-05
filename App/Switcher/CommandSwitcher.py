import App/VoiceAssistant.py
from App/Utils/Enums import Command
import Google/GoogleSearch.py

class Switcher:
    def __init__(self,voice):
        self.__google_search = None
        self.__openApp = None
        
    def switch(self,command):
        if command == Command.google_search:
            return searchGoogle()
        elif command == Command.run_application:
            return openApp()
    
    def searchGoogle(self):
        if self.__google_search is None:
            self.__google_search = GoogleSearch(voice)
        self.__google_search.search()
    
    def openApp()
        
import webbrowser
from App.VoiceAssistant import VoiceAssistant


class GoogleSearch:
    def __init__(self, mediator: VoiceAssistant):
        self.__mediator = mediator

    def search(self):
        url = "https://www.google.com/search?q=" + self.__mediator.get_request()
        webbrowser.open(url)

  


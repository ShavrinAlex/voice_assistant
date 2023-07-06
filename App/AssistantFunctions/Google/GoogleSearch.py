import webbrowser
from App.VoiceAssistant import VoiceAssistant


class GoogleSearch:
    def __init__(self, mediator: VoiceAssistant):
        self.__mediator = mediator

    def search(self):
        self.__mediator.reproduce_speech("прошу, введите ваш запрос")
        request = self.__mediator.get_request()
        url = "https://www.google.com/search?q=" + request
        webbrowser.open(url)
        self.__mediator.reproduce_speech("вот что мне удалось найти по запросу: " + request)

  


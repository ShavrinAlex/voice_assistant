import webbrowser
from App.VoiceAssistant import VoiceAssistant


class GoogleSearcher:
    """
    Этот класс осуществляет поиск информации в интернете
    This class searches for information on the Internet.
    """

    def __init__(self, mediator: VoiceAssistant) -> None:
        self.__mediator = mediator

    def search(self) -> None:
        """
        Функция непосредственного поиска
        Direct search function
        """

        self.__mediator.reproduce_speech("прошу, скажите, что нужно найти")
        request = self.__mediator.get_request()
        url = "https://www.google.com/search?q=" + request
        webbrowser.open(url)
        self.__mediator.reproduce_speech("вот что мне удалось найти по запросу: " + request)

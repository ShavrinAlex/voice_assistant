from AppOpener import open, close
import translate
import string
from App.VoiceAssistant import VoiceAssistant


class OpenApp:
    """
    Класс, реализующий открытые приложения на компьютере
    Class that implements open applications on a computer
    """

    def __init__(self, mediator: VoiceAssistant) -> None:
        self.__mediator = mediator
        self.__app = ""
        self.__command = ""
        self.__nonrequest_words = ["a", "the", "open", "find", "on", "computer", "please", "good", "evening", "morning",
                                   "afternoon", "night", "my", "me", "i", "you", "your", "close", "can", "hi", "hello",
                                   "how", "bad", "are", "am", "is", "for", "would", "want", "like" ,"to", "in", "at",
                                   "on", "game", "program", "application"]

    def __command_transform(self, input_string: str) -> None:
        """
        Этот метод осуществляет преобразование пользовательской командной строки в строку имени приложения
        This method of converting a custom command line to an application name string
        """

        translator = translate.Translator("en", "ru")
        input_string_words = translator.translate(input_string).lower()
        input_string_words = input_string_words.translate(str.maketrans('', '', string.punctuation))
        input_string_words = input_string_words.split()
        request_words = []
        for word in input_string_words:
            if word == "open" or word == "close":
                self.__command = word
            if word not in self.__nonrequest_words:
                request_words.append(word)
        if len(request_words) == 0:
            self.__mediator.reproduce_speech("К сожалению, я не не знаю такого приложения")
            return
        self.__app = ' '.join(request_words)

    def __find_app(self) -> None:
        """
        Этот метод осуществляет использование библиотеки AppOpener для открытия/закрытия приложения
        This method uses the AppOpener library to open/close the application
        """

        try:
            if self.__command == "open":
                open(self.__app,match_closest=True,throw_error=True)
            elif self.__command == "close":
                close(self.__app,match_closest=True,throw_error=True)
            else:
                self.__mediator.reproduce_speech("К сожалению, я не понимаю такой команды для работы с приложениями")
                pass
        except:
            self.__mediator.reproduce_speech("К сожалению, я не понимаю такой команды для работы с приложениями")
            pass
        pass

    def open_app(self, input_string: str) -> None:
        """
        Метод, вызываемый для работы с классом
        Method called to work with the class
        """

        try:
            self.__command_transform(input_string)
            print(self.__command)
            print(self.__app)
            self.__find_app()
        except:
            print("exception")
            self.__mediator.reproduce_speech("К сожалению, я не понимаю такой команды для работы с приложениями")

from AppOpener import open, close
import translate
import string


class OpenApp:
    """
    class that implements open applications on a computer
    """
    def __init__(self):
        self.__app = ""
        self.__command = ""
        self.__nonrequest_words = ["a", "the", "open", "find", "on", "computer", "please", "good", "evening", "morning", "afternoon", "night",
                                 "my","me","i","you","your","close","can","hi","hello","how","bad","are","am","is","for","would","want",
                                 "like","to","in","at","on","game","program","application"]

    def __command_transform(self, input_string: str):
        """
        Converting a user command string to an application name string
        :return:
        """

        translator = translate.Translator("en","ru")
        input_string_words = translator.translate(input_string).lower()
        input_string_words = input_string_words.translate(str.maketrans('', '', string.punctuation))
        input_string_words = input_string_words.split()
        request_words = []
        for word in input_string_words:
            if word == "open" or word == "close":
                self.__command = word
            if word not in self.__nonrequest_words:
                request_words.append(word)
        if len(request_words)==0:
            # Exception Unknown command
            pass
        self.__app = ' '.join(request_words)

    def __find_app(self):
        """
        Using the AppOpener library to open/close an application
        :return:
        """

        try:
            if self.__command == "open":
                open(self.__app,match_closest=True,throw_error=True)
            elif self.__command == "close":
                close(self.__app,match_closest=True,throw_error=True)
            else:
                print("exception")
                #exeption Unknown command
                pass
        except:
            print("exeption")
            #Exception Unknown command
            pass
        pass

    def open_app(self, input_string: str):
        """
        Method called to work with the class
        :return:
        """

        try:
            self.__command_transform(input_string)
            print(self.__command)
            print(self.__app)
            self.__find_app()
        except:
            print("exception")
            #exception Unknown command

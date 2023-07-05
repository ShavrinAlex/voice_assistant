from App.SpeechReceiver.SpeechReceiver import SpeechReceiver
from App.SpeechReproducer.SpeechReproduser import SpeechReproducer
from App.CommandRecognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Config import VA_NAME
from App.Utils.Enums import Command
import os  # working with the file system

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
    # from App.AssistantFunctions.Reminder import Reminder


class VoiceAssistant:
    """
    Класс-фасад. Вызывается из main, реализует главный цикл программы.
    Хранит, принимает и отдает информацию.
    Class-facade. Called from main, implements the main program loop.
    Stores, accepts and gives information.
    """

    def __init__(self):
        self.__speech_reproduces = SpeechReproducer()
        self.__speech_receiver = SpeechReceiver()
        self.__command_recognizer = CommandRecognizer()

        self.__speech_string = ""
        self.__wake_word = VA_NAME

    def start(self):
        """
        Основной уикл работы программы. Запускает остальные модули и принимает от них данные.
        The main loop of the program. Launches the other modules and receives data from them.
        :return:
        """
        self.__speech_receiver.wake_word_detection()
        self.__speech_reproduces.reproduce_greetings()
        while True:
            # старт записи речи с последующим выводом распознанной речи
            # и удалением записанного в микрофон аудио
            self.__speech_string = self.get_request()

            command = self.__command_recognizer.get_command(self.__speech_string)

            # Перенести в CommandSwitcher
            if (command == Command.farewell):
                self.__speech_reproduces.reproduce_farewell_and_quit()
                break
            elif (command == Command.greeting):
                self.__speech_reproduces.reproduce_greetings()
            # elif (command == Command.failure):
            #     self.__speech_reproduces.reproduce_failure_phrase()
            elif (self.__speech_string == "напомни"):
                from App.AssistantFunctions.Reminder import Reminder
                rem = Reminder(self)
                rem.create_promt()
    
    def get_request(self):
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        self.__speech_reproduces.reproduce_speech('Слушаю')
        speech_string = self.__speech_receiver.record_and_recognize_audio()

        if os.path.exists("microphone-results.wav"):
            os.remove("microphone-results.wav")
        print(speech_string)
        return speech_string
    
    def reproduce_speech(self, string_to_reproduce: str):
        self.__speech_reproduces.reproduce_speech(string_to_reproduce)

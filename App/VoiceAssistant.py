from App.SpeechReceiver.SpeechReceiver import SpeechReceiver
from App.SpeechReproducer.SpeechReproduser import SpeechReproducer
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Config import VA_NAME
from App.Utils.Enums import Commands
import os  # working with the file system
import datetime


# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from App.AssistantFunctions.Reminder.ReminderChecker import ReminderChecker

COMMANDS_FILE = 'App/Recognizer/config.json'
INDEX_OF_PROBABILITY = 0.2


class VoiceAssistant:
    """
    Класс голосового ассистента - фасад. Вызывается из main, реализует главный цикл программы.
    Хранит, принимает и отдает информацию. Он имеет следующие поля:
    Voice assistant class - facade. Called from main, implements the main loop of the program.
    Stores, accepts and gives information. It has the following fields:

    :field __speech_reproduces: SpeechReproducer - объект для воспроизведения ответов помощника
    :field __speech_receiver: SpeechReceiver - объект распознавания голоса в текст
    :field __command_recognizer: Recognizer - объект распознавателя команд в пользовательском тексте
    :field __speech_string: string - прочитанная пользователем фраза
    :field __wake_word: string - пробуждающее слово-фраза

    :field __speech_reproduces: SpeechReproducer - object for reproducing the assistant's responses
    :field __speech_receiver: SpeechReceiver - voice recognition object to text
    :field __command_recognizer: Recognizer - the command recognizer object in the user's text
    :field __speech_string: string - the user's read phrase
    :field __wake_word: string - wake word phrase
    """

    def __init__(self):
        self.__speech_reproduces = SpeechReproducer()
        self.__speech_receiver = SpeechReceiver()
        self.__command_recognizer = CommandRecognizer(Commands, COMMANDS_FILE, INDEX_OF_PROBABILITY)

        self.__speech_string = ""
        self.__wake_word = VA_NAME
        self.__running = False
        self.__reminder_checker = ReminderChecker()

    def start(self) -> None:
        """
        Основной уикл работы программы. Запускает остальные модули и принимает от них данные.
        The main loop of the program. Launches the other modules and receives data from them.
        """

        from App.Switcher.CommandSwitcher import Switcher
        self.__command_switcher = Switcher(self)
        self.__running = True
        print("program started")
        self.__speech_receiver.wake_word_detection()
        self.__speech_reproduces.reproduce_greetings()
        self.__reminder_checker.check_events()

        while self.__running:
            now = datetime.datetime.now()
            if now.hour == 0 and now.minute == 0:
                self.__reminder_checker.check_events()

            self.__speech_string = self.get_request()
            command = self.__command_recognizer.get_command(self.__speech_string)
            self.__command_switcher.switch(command, self.__speech_string)
    
    def get_request(self) -> str:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        self.__speech_reproduces.reproduce_speech('Слушаю')
        speech_string = self.__speech_receiver.record_and_recognize_audio()

        if os.path.exists("microphone-results.wav"):
            os.remove("microphone-results.wav")
        print(speech_string)
        return speech_string
    
    def reproduce_speech(self, string_to_reproduce: str) -> None:
        self.__speech_reproduces.reproduce_speech(string_to_reproduce)
    
    def stop_app(self) -> None:
        self.__running = False
    
    def reproduce_greetings(self) -> None:
        self.__speech_reproduces.reproduce_greetings()

    def reproduce_farewell_and_quit(self) -> None:
        self.__speech_reproduces.reproduce_farewell_and_quit()

from App.SpeechReceiver.SpeechReceiver import SpeechReceiver
from App.SpeechReproducer.SpeechReproduser import SpeechReproducer
from App.CommandRecognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Config import VA_NAME
from App.Utils.Enums import Command
import os  # working with the file system


class VoiceAssistant:
    """
    Класс голосового ассистента - фасад. Вызывается из main, реализует главный цикл программы.
    Хранит, принимает и отдает информацию. Он имеет следующие поля:
    Voice assistant class - facade. Called from main, implements the main loop of the program.
    Stores, accepts and gives information. It has the following fields:

    :field __speech_reproduces: SpeechReproducer - объект для воспроизведения ответов помощника
    :field __speech_receiver: SpeechReceiver - объект распознавания голоса в текст
    :field __command_recognizer: CommandRecognizer - объект распознавателя команд в пользовательском тексте
    :field __speech_string: string - прочитанная пользователем фраза
    :field __wake_word: string - пробуждающее слово-фраза

    :field __speech_reproduces: SpeechReproducer - object for reproducing the assistant's responses
    :field __speech_receiver: SpeechReceiver - voice recognition object to text
    :field __command_recognizer: CommandRecognizer - the command recognizer object in the user's text
    :field __speech_string: string - the user's read phrase
    :field __wake_word: string - wake word phrase
    """

    def __init__(self):
        self.__speech_reproduces = SpeechReproducer()
        self.__speech_receiver = SpeechReceiver()
        self.__command_recognizer = CommandRecognizer()

        self.__speech_string = ""
        self.__wake_word = VA_NAME

    def start(self) -> None:
        """
        Основной уикл работы программы. Запускает остальные модули и принимает от них данные.
        The main loop of the program. Launches the other modules and receives data from them.
        """

        print("program started")
        self.__speech_receiver.wake_word_detection()
        self.__speech_reproduces.reproduce_greetings()

        while True:
            # старт записи речи с последующим выводом распознанной речи
            # и удалением записанного в микрофон аудио
            self.__speech_reproduces.reproduce_speech('Слушаю')
            self.__speech_string = self.__speech_receiver.record_and_recognize_audio()

            if os.path.exists("microphone-results.wav"):
                os.remove("microphone-results.wav")
            print(self.__speech_string)

            command = self.__command_recognizer.get_command(self.__speech_string)

            # Перенести в CommandSwitcher
            if (command == Command.farewell):
                self.__speech_reproduces.reproduce_farewell_and_quit()
                break
            elif (command == Command.greeting):
                self.__speech_reproduces.reproduce_greetings()
            elif (command == Command.failure):
                self.__speech_reproduces.reproduce_failure_phrase()

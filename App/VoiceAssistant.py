from App.SpeechReceiver.SpeechReceiver import SpeechReceiver
from App.SpeechReproducer.SpeechReproduser import SpeechReproducer
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Config import VA_NAME
from App.Utils.Enums import Commands
import os  # working with the file system


# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
    # from App.AssistantFunctions.Reminder import Reminder
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
            self.__speech_string = self.get_request()

            command = self.__command_recognizer.get_command(self.__speech_string)

            # Перенести в CommandSwitcher
            if (command == Commands.farewell):
                self.__speech_reproduces.reproduce_farewell_and_quit()
                break
            elif (command == Commands.greeting):
                self.__speech_reproduces.reproduce_greetings()
            # elif (command == Command.failure):
            #     self.__speech_reproduces.reproduce_failure_phrase()
            elif (self.__speech_string == "напомни"):
                from App.AssistantFunctions.Reminder import Reminder
                rem = Reminder(self)
                rem.create_promt()
            elif (command == Commands.run_application):
                from App.AppOpener.OpenApp import OpenApp
                oa = OpenApp(self.__speech_string)
                oa.open_app()
            elif (command == Commands.volume_settings):
                from App.SoundController.SoundController import SoundController
                sc = SoundController()
                sc.execute(self.__speech_string)
            elif (command == Commands.screen_brightness_settings):
                from App.ScreenBrightnessController.ScreenBrightnessController import ScreenBrightnessController
                sbc = ScreenBrightnessController()
                sbc.execute(self.__speech_string)

    
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

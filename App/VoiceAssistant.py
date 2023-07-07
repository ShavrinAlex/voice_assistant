from App.SpeechReceiver.SpeechReceiver import SpeechReceiver
from App.SpeechReproducer.SpeechReproduser import SpeechReproducer
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Config import VA_NAME
from App.Utils.Enums import GeneralCommands
import os  # working with the file system
import datetime
from App.AssistantFunctions.Reminder.ReminderChecker import ReminderChecker


COMMANDS_FILE = 'App/Recognizer/config.json'
INDEX_OF_PROBABILITY = 0.2
COUNT_DIALOGS = 2


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

    def __init__(self) -> None:
        self.__speech_reproduces = SpeechReproducer()
        self.__speech_receiver = SpeechReceiver()
        self.__command_recognizer = CommandRecognizer(GeneralCommands, COMMANDS_FILE, INDEX_OF_PROBABILITY)

        self.__speech_string = ""
        self.__wake_word = VA_NAME
        self.__running = False
        self.__reminder_checker = ReminderChecker()
        self.__first_dialog = True

    def start(self) -> None:
        """
        Основной уикл работы программы. Запускает остальные модули и принимает от них данные.
        The main loop of the program. Launches the other modules and receives data from them.
        """

        from App.CommandsSwitcher.CommandSwitcher import CommandsSwitcher
        self.__command_switcher = CommandsSwitcher(self)
        self.__reminder_checker.check_events()
        self.__running = True
        print("program started")

        while self.__running:
            now = datetime.datetime.now()
            if now.hour == 0 and now.minute == 0:
                self.__reminder_checker.check_events()

            self.__speech_receiver.wake_word_detection()

            if self.__first_dialog:
                self.__speech_reproduces.reproduce_greetings()
                self.__first_dialog = False

            self.dialog()

    def dialog(self) -> None:
        """
        Этот метод реализует общение с пользователем ограниченное число раз, в случае если все разы пользователь
        не сказал ничего, то ассистент выходит из функции и снова ожидает активационную фразу, если же пользователь
        дал команду, данный метод запускается рекурсивно
        This method implements communication with the user a limited number of times, if the user
        has not said anything all the times, the assistant exits the function and waits for the activation phrase again, if the user
        has given a command, this method is run recursively
        """

        for i in range(COUNT_DIALOGS):
            self.__speech_string = self.get_request()
            command = self.__command_recognizer.get_command(self.__speech_string)
            self.__command_switcher.switch(command, self.__speech_string)

            if command == GeneralCommands.farewell:
                return
            if command != GeneralCommands.failure:
                self.dialog()
                return

    def get_request(self) -> str:
        """
        Эта функция осуществляет старт записи речи с последующим выводом распознанной речи
        и удалением записанного в микрофон аудио
        This function starts speech recording, then outputs the recognized speech
        and removes the audio recorded in the microphone.

        :return: string - распознанная речь
        :return: string - recognized speech
        """

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
        self.stop_app()

    def reproduce_failure_phrase(self) -> None:
        self.__speech_reproduces.reproduce_failure_phrase()

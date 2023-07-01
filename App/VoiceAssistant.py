from App.SpeechReceiver.SpeechReceiver import SpeechReceiver
from App.SpeechReproducer.SpeechReproduser import SpeechReproducer
from App.Utils.Config import VA_NAME
import os  # working with the file system


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

        self.__speech_string = ""
        self.__wake_word = VA_NAME

    def start(self):
        """
        Основной уикл работы программы. Запускает остальные модули и принимает от них данные.
        The main loop of the program. Launches the other modules and receives data from them.
        :return:
        """

        self.__speech_reproduces.reproduce_greetings()
        start_work_flag = False
        #while self.SpeechReceiver.wake_word_detection() == False: #заглушка для реализации с wwd
            #continue
        while True:
            # старт записи речи с последующим выводом распознанной речи
            # и удалением записанного в микрофон аудио
            self.__speech_reproduces.reproduce_speech('Слушаю')
            self.__speech_string = self.__speech_receiver.record_and_recognize_audio()
            if os.path.exists("microphone-results.wav"):
                os.remove("microphone-results.wav")
            print(self.__speech_string)
            if (self.__speech_string == 'пока'):
                self.__speech_reproduces.reproduce_farewell_and_quit()
            if start_work_flag == False: #первоначальная версия, с добавлением wwd будет удалено
                start_work_flag = self.is_wake_word()

            if start_work_flag:
                # дальнейшая реализация command recognition
                print("Начало работы")
                return

    def is_wake_word(self) -> bool:
        """
        Проверка, сказано ли пользователем "wake word" для начала работы
        Checking whether the user says "wake word" to get started
        :return:
        """
        return self.__speech_string == self.__wake_word
        pass
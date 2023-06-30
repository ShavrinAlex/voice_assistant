import app.receive_speech.receive_speech as receive
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import os  # работа с файловой системой

WAKE_WORD = "очевидно"


class Voice_Assistent:
    '''
    Класс-фасад. Вызывается из main, реализует главный цикл программы.
    Хранит, принимает и отдает информацию.
    Class-facade. Called from main, implements the main program loop.
    Stores, accepts and gives information.
    '''

    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.receive_speech = receive.Receive_Speech()
        self.speech_string = ""
        self.wake_word = WAKE_WORD
        pass

    def start(self):
        '''
        Основной уикл работы программы. Запускает остальные модули и принимает от них данные.
        The main loop of the program. Launches the other modules and receives data from them.
        :return:
        '''
        start_work_flag = False
        #while self.receive_speech.wake_word_detection() == False: #заглушка для реализации с wwd
            #continue
        while True:
            # старт записи речи с последующим выводом распознанной речи
            # и удалением записанного в микрофон аудио
            self.speech_string = self.receive_speech.record_and_recognize_audio(self.recognizer, self.microphone)
            if os.path.exists("microphone-results.wav"):
                os.remove("microphone-results.wav")
            print(self.speech_string)
            if start_work_flag == False: #первоначальная версия, с добавлением wwd будет удалено
                start_work_flag = self.is_wake_word()

            if start_work_flag:
                # дальнейшая реализация command recognition
                print("Начало работы")
                return

    def is_wake_word(self) -> bool:
        '''
        Проверка, сказано ли пользователем "wake word" для начала работы
        Checking whether the user says "wake word" to get started
        :return:
        '''
        return self.speech_string == self.wake_word
        pass

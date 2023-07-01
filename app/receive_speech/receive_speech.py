from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import speech_recognition # распознавание пользовательской речи (Speech-To-Text)
import os  # работа с файловой системой


class Receive_Speech:
    '''
    Принимает и обрабатывает речь пользователя. Возвращает в класс основной программы строку, сказанную пользователем
    Accepts and processes the user's speech. Returns to the class of the main program the string said by the user
    '''

    def __init__(self):
        pass
    def record_and_recognize_audio(self,recognizer,microphone,*args: tuple):
        '''
        :param args:
        :param recognizer: распознаватель, объект из библиотеки speech_recognition
        :param microphone: микрофон, объект из библиотеки speech_recognition
        :return: строка, сказанная пользователем
        '''
        with microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            recognizer.adjust_for_ambient_noise(microphone, duration=2)

            try:
                print("Listening...")
                audio = recognizer.listen(microphone, 5, 5)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            # использование online-распознавания через Google
            try:
                print("Started recognition...")
                recognized_data = recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                pass

            # в случае проблем с доступом в Интернет происходит попытка
            # использовать offline-распознавание через Vosk
            except speech_recognition.RequestError:
                print("Trying to use offline recognition...")
                recognized_data = self.use_offline_recognition()

            return recognized_data

    def use_offline_recognition(self):
        """
        Переключение на оффлайн-распознавание речи
        :return: распознанная фраза
        """
        recognized_data = ""
        try:
            # проверка наличия модели на нужном языке в каталоге приложения
            if not os.path.exists("models/vosk-model-small-ru-0.4"):
                print("Please download the model from:\n"
                      "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
                exit(1)

            # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
            wave_audio_file = wave.open("microphone-results.wav", "rb")
            model = Model("models/vosk-model-small-ru-0.4")
            offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

            data = wave_audio_file.readframes(wave_audio_file.getnframes())
            if len(data) > 0:
                if offline_recognizer.AcceptWaveform(data):
                    recognized_data = offline_recognizer.Result()

                    # получение данных распознанного текста из JSON-строки
                    # (чтобы можно было выдать по ней ответ)
                    recognized_data = json.loads(recognized_data)
                    recognized_data = recognized_data["text"]
        except:
            print("Sorry, speech service is unavailable. Try again later")

        return recognized_data

    def wake_word_detection(self) -> bool:
        '''
        используя модуль porcupine находит слово для активации голосового асистента
        :return: Флаг, уведомляющий о том, что wake word найдено.
        '''
        pass

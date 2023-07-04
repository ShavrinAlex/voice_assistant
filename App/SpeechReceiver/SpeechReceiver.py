from vosk import Model, KaldiRecognizer     # offline recognition from Vosk
import wave                                 # creating and reading wav audio files
import json                                 # working with json files and json strings
import speech_recognition                   # user speech recognition (Speech-To-Text)
import os                                   # working with the file system
import pvporcupine                          # wake word detection library
from pvrecorder import PvRecorder           # record wake word detection
from pathlib import Path                    # build path to file


LAST_KEYWORDS_PATH = 'venv/Lib/site-packages/pvporcupine/resources/keyword_files/windows/wwd_ru.ppn'
ACCESS_KEY = "1UuJKwXkKEHtVKZe8fwNET4gcDhPDuYfLKs8vRcVP8Z8bF1xZBnyUw=="
LAST_MODEL_PATH = 'venv/Lib/site-packages/pvporcupine/lib/common/porcupine_params_ru.pv'


class SpeechReceiver:
    """
    Класс получатель речи. Принимает и обрабатывает речь пользователя. Он имеет следующие поля:
    The speech recipient class. Accepts and processes the user's speech. It has the following fields:

    :field __recognizer: speech_recognition.Recognizer - обьект распознавателя из библиотеки speech_recognition
    :field __microphone: speech_recognition.Microphone - обьект микрофона из библиотеки speech_recognition

    :field __recognizer: speech_recognition.Recognizer - the recognizer object from the speech_recognition library
    :field __microphone: speech_recognition.Microphone - microphone object from the speech_recognition library
    """

    def __init__(self):
        self.__recognizer = speech_recognition.Recognizer()
        self.__microphone = speech_recognition.Microphone()

        with self.__microphone:
            # регулирование уровня окружающего шума
            self.__recognizer.adjust_for_ambient_noise(self.__microphone, duration=2)

    def record_and_recognize_audio(self) -> str:
        """
        Этот метод записывает команду пользователя и переводит ее в текст, используя сеть
        This method records the user's command and translates it into text using the network

        :return: строка, сказанная пользователем
        :return: a string said by the user
        """

        with self.__microphone:
            recognized_data = ""
            try:
                print("Listening...")
                audio = self.__recognizer.listen(self.__microphone, 5, 5)

                with open("microphone-results.wav", "wb") as file:
                    file.write(audio.get_wav_data())

            except speech_recognition.WaitTimeoutError:
                print("Can you check if your microphone is on, please?")
                return

            # использование online-распознавания через Google
            try:
                print("Started recognition...")
                recognized_data = self.__recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                pass

            # в случае проблем с доступом в Интернет происходит попытка
            # использовать offline-распознавание через Vosk
            except speech_recognition.RequestError:
                print("Trying to use offline recognition...")
                recognized_data = self.use_offline_recognition()

            return recognized_data

    def use_offline_recognition(self) -> str:
        """
        Этот метод переводит команду пользователя в текст, не используя сеть
        This method translates the user's command into text without using the network

        :return: строка - распознанная фраза
        :return: string - recognized phrase
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

    def wake_word_detection(self):
        """
        Этот метод, используя модуль porcupine находит слово для активации голосового ассистента
        This method, using the porcupine module, finds the word to activate the voice assistant

        :return: Флаг, уведомляющий о том, что wake word найдено.
        :return: Flag notifying that wake word has been found.
        """

        work_dir = Path('').resolve()   # получает путь до папки проекта
        access_key = ACCESS_KEY
        keywords_path = [str(work_dir/LAST_KEYWORDS_PATH)]
        model_path = str(work_dir/LAST_MODEL_PATH)
        porcupine = pvporcupine.create(access_key=access_key, keyword_paths=keywords_path,
                                       model_path=model_path)
        recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

        print("wwd started")
        try:
            recoder.start()
            while True:
                keyword_index = porcupine.process(recoder.read())
                if keyword_index >= 0:
                    print('wake word detected,program start')
                    break
        except KeyboardInterrupt:
            recoder.stop()
        finally:
            porcupine.delete()
            recoder.delete()
        pass

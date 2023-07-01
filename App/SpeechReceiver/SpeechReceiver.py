from vosk import Model, KaldiRecognizer     # offline recognition from Vosk
import wave                                 # creating and reading wav audio files
import json                                 # working with json files and json strings
import speech_recognition                   # user speech recognition (Speech-To-Text)
import os                                   # working with the file system
import pvporcupine                          # wake word detection library
from pvrecorder import PvRecorder           # record wake word detection
from pathlib import Path                    # build path to file

LAST_KEYWORDS_PATH = 'venv/Lib/site-packages/pvporcupine/resources/keyword_files/windows/wwd_ru.ppn'
ACCESS_KEY = "ovnQ/QcjpAvIZin1XfxN0ZeWQOG3Iy3EdxF+J9SM0+jStZBzZ774Ow=="
LAST_MODEL_PATH = 'venv/Lib/site-packages/pvporcupine/lib/common/porcupine_params_ru.pv'

class SpeechReceiver:
    """
    Принимает и обрабатывает речь пользователя. Возвращает в класс основной программы строку, сказанную пользователем
    Accepts and processes the user's speech. Returns to the class of the main program the string said by the user
    """

    def __init__(self):
        self.__recognizer = speech_recognition.Recognizer()
        self.__microphone = speech_recognition.Microphone()

    def record_and_recognize_audio(self) -> str:
        """
        :return: строка, сказанная пользователем
        """

        with self.__microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            self.__recognizer.adjust_for_ambient_noise(self.__microphone, duration=2)

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

    def wake_word_detection(self):
        '''
        используя модуль porcupine находит слово для активации голосового асистента
        :return: Флаг, уведомляющий о том, что wake word найдено.
        '''
        project_path = open(str(Path('App/SpeechReceiver/ProjectPath.txt')),'r')
        work_dir = Path(project_path.read())
        access_key = ACCESS_KEY
        keywords_path = [str(work_dir/LAST_KEYWORDS_PATH)]
        model_path = str(work_dir/LAST_MODEL_PATH)
        porcupine = pvporcupine.create(access_key=access_key, keyword_paths=keywords_path,
                                       model_path=model_path)
        recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

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

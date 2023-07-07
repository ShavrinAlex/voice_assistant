from App.Utils.Config import *
from App.Utils.Enums import Sex, Languages
import pyttsx3                                          # for voice playback on Windows
import os.path                                          # to get the path to the data file
from App.PickleLoader.PickleLoader import PickleLoader  # to save the settings
from time import time


class SpeechReproducer:
    """
    Класс воспроизводителя голосового помощника, который включает в себя следующие поля:
    Voice assistant reproducer class, which includes the following fields:

    :field __name: строка - имя голосового помощника
    :field __sex: строка - пол голосового помощника
    :field __language: строка - язык, который распознает помощник, и речь
    :field __voice_engine: строка - pyttsx3.Engine - голосовой движок

    :field __name: string - name of the voice assistant
    :field __sex: string - voice assistant's gender
    :field __language: string - the language that the assistant recognizes and speech
    :field __voice_engine: string - pyttsx3.Engine - voice engine
    """

    def __init__(self, name=VA_NAME, sex=VA_SEX, language=VA_LANGUAGE) -> None:
        file_to_load = os.path.abspath(VA_DATA_FILE)
        if os.path.exists(file_to_load):
            self.__name, self.__sex, self.__language = PickleLoader.load(file_to_load)
        else:
            self.__name, self.__sex, self.__language = name, sex, language
            data = [name, sex, language]
            PickleLoader.dump(data,  file_to_load)

        self.__voice_engine = self.set_voice()

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_sex(self, sex: str) -> None:
        if sex in Sex:
            self.__sex = Sex[sex].value

    def set_language(self, language: str) -> None:
        if language in Languages:
            self.__language = language

    def set_voice(self) -> pyttsx3.Engine:
        """
        Эта функция устанавливает голос помощника по умолчанию
        (индекс может варьироваться в зависимости от настроек операционной системы)
        This function sets the assistant's voice by default
        (the index may vary depending on the operating system settings)

        :return tts_engine: pyttsx 3.Engine - голосовой движок
        :return tts_engine: pyttsx3.Engine - voice engine
        """

        tts_engine = pyttsx3.init()
        voices = tts_engine.getProperty("voices")

        voices_configurations = {(Languages.RU.value, Sex.Woman.value): voices[0].id,  # Irina - Russian
                                 (Languages.EN.value, Sex.Woman.value): voices[1].id,  # Zira - English (United States)
                                 }

        try:
            tts_engine.setProperty("voice", voices_configurations[(self.__language, self.__sex)])
        except KeyError:
            print('No voice for this configuration. The standard value is set to: Woman, RU')
            self.__language, self.__sex = Languages.RU.value, Sex.Woman.value
            tts_engine.setProperty("voice", voices_configurations[(Languages.RU.value, Sex.Woman.value)])

        tts_engine.setProperty('rate', 265)
        tts_engine.setProperty('volume', 0.9)

        return tts_engine

    def reproduce_speech(self, text_to_speech: str) -> None:
        """
        Эта функция воспроизводит речь в ответах голосового помощника (без сохранения звука)
        This function plays the speech of the voice assistant's responses (without saving audio)

        :param text_to_speech: строка - текст, подлежащий преобразованию в речь
        :param text_to_speech: string - text to be converted to speech
        """

        self.__voice_engine.say(text_to_speech)
        self.__voice_engine.runAndWait()

    def reproduce_greetings(self) -> None:
        """
        Эта функция воспроизводит случайную приветственную фразу
        This function plays a random welcome phrase
        """

        greetings = [
            "Привет! Чем я могу помочь вам сегодня?",
            "Доброго вам дня! Чем я могу помочь вам сегодня?"
        ]
        self.reproduce_speech(greetings[int(time() % len(greetings))])

    def reproduce_failure_phrase(self) -> None:
        """
        Эта функция воспроизводит случайную фразу при сбое распознавания
        This function plays a random phrase when recognition fails
        """

        failure_phrases = [
            'Извини, я не поняла, что ты сказал',
            'К сожалению, мне не удалось распознать комманду'
        ]
        self.reproduce_speech(failure_phrases[int(time() % len(failure_phrases))])

    def reproduce_farewell_and_quit(self) -> None:
        """
        Эта функция воспроизводит прощальную речь и завершает работу ассистента
        This function plays the farewell speech and completes the assistant's work
        """

        # нужно добавить перевод по необходимости и вывод данных о пользователе
        farewells = [
            "Прощай! Хорошего дня!",
            "Скоро увидимся!"
        ]
        self.reproduce_speech(farewells[int(time() % len(farewells))])
        self.__voice_engine.stop()

from App.Utils.Config import *
from App.Utils.Enums import Sex, Languages
import pyttsx3                                          # for voice playback on Windows
import os.path                                          # to get the path to the data file
from App.PickleLoader.PickleLoader import PickleLoader  # to save the settings
from random import randint


class SpeechReproducer:
    """
    Voice assistant reproducer class, which includes the following fields:
    :field __name: string - name of the voice assistant
    :field __sex: string - voice assistant's gender
    :field __language: string - the language that the assistant recognizes and speech
    :field __voice_engine: string - pyttsx3.Engine - voice engine
    """

    def __init__(self, name=VA_NAME, sex=VA_SEX, language=VA_LANGUAGE):
        d = os.path.abspath(VA_DATA_FILE)
        if os.path.exists(d):
            self.__name, self.__sex, self.__language = PickleLoader.load(d)
        else:
            self.__name, self.__sex, self.__language = name, sex, language
            data = [name, sex, language]
            PickleLoader.dump(data, d)

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
        This function sets the assistant's voice by default
        (the index may vary depending on the operating system settings)
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

        return tts_engine

    def reproduce_speech(self, text_to_speech: str) -> None:
        """
        This function plays the speech of the voice assistant's responses (without saving audio)
        :param text_to_speech: string - text to be converted to speech
        """

        self.__voice_engine.say(text_to_speech)
        self.__voice_engine.runAndWait()

    def reproduce_greetings(self):
        """
        This function plays a random welcome phrase
        """
        # нужно добавить перевод по необходимости и вывод данных о пользователе
        greetings = [
            "Привет, {}! Чем я могу помочь вам сегодня?",
            "Доброго вам дня {}! Чем я могу помочь вам сегодня?"
        ]
        self.reproduce_speech(greetings[randint(0, len(greetings) - 1)])

    def reproduce_failure_phrase(self) -> None:
        """
        This function plays a random phrase when recognition fails
        """

        # нужно добавить перевод по необходимости
        failure_phrases = [
            'Не могли бы вы повторить, пожалуйста?',
            'Повтори, что ты сказал?'
        ]
        self.reproduce_speech(failure_phrases[randint(0, len(failure_phrases) - 1)])

    def reproduce_farewell_and_quit(self):
        """
        This function plays the farewell speech
        """

        # нужно добавить перевод по необходимости и вывод данных о пользователе
        farewells = [
            "Прощай, {}! Хорошего дня!",
            "Скоро увидимся, {}!"
        ]
        self.reproduce_speech(farewells[randint(0, len(farewells) - 1)])
        self.__voice_engine.stop()
        quit()
#s = SpeechReproducer()
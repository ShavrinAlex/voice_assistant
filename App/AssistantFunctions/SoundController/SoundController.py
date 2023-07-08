from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Enums import VolumeCommands
from App.VoiceAssistant import VoiceAssistant


COMMANDS_FILE = 'App/AssistantFunctions/SoundController/Commands.json'
INDEX_OF_PROBABILITY = 0.3


class SoundController:
    """
    Класс контроллера звука осуществляет изменение громкости звука на компьютере и включает следующие поля:
    The sound controller class changes the sound volume on the computer and includes the following fields:

    :field __devices: список - устройства вывода звука
    :field __interface: активное устройство вывода звука
    :field __volume: интерфейс работы со звуком активного устройства вывода

    :field __devices: list - audio output devices
    :field __interface: active audio output device
    :field __volume: interface for working with the sound of the active output device
    """

    def __init__(self, mediator: VoiceAssistant, volume_delta=10) -> None:
        self.__mediator = mediator
        self.__devices = AudioUtilities.GetSpeakers()
        self.__interface = self.__devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.__volume = self.__interface.QueryInterface(IAudioEndpointVolume)
        self.__cmd_recognizer = CommandRecognizer(VolumeCommands, COMMANDS_FILE, INDEX_OF_PROBABILITY)
        self.__volume_delta = volume_delta    # параметр на сколько увеличивать или уменьшать звук

    def __get_volume_value(self, command_string: str) -> int:
        try:
            return int(''.join(filter(str.isdigit, command_string)))
        except ValueError:
            return -1

    def mute(self) -> None:
        self.__volume.SetMute(1, None)

    def unmute(self) -> None:
        self.__volume.SetMute(0, None)

    def get_volume(self) -> int:
        return int(self.__volume.GetMasterVolumeLevelScalar() * 100)

    def set_volume(self, volume_percentage: int) -> None:
        self.__volume.SetMasterVolumeLevelScalar(volume_percentage / 100, None)

    def execute(self, command_string: str) -> None:
        command = self.__cmd_recognizer.get_command(command_string)
        if command == VolumeCommands.set_value:
            volume_percentage = self.__get_volume_value(command_string)
            if 0 <= volume_percentage <= 100:
                self.set_volume(volume_percentage)
                self.__mediator.reproduce_speech(f"Громкость звука {volume_percentage}")
            else:
                self.__mediator.reproduce_speech("Некорректное значение громкости, повторите еще раз")

        elif command == VolumeCommands.mute:
            self.__mediator.reproduce_speech("Звук выключен")
            self.mute()

        elif command == VolumeCommands.unmute:
            self.unmute()
            self.__mediator.reproduce_speech("Звук включен")

        elif command == VolumeCommands.up:
            current_volume = self.get_volume()
            delta_volume_value = self.__get_volume_value(command_string)
            if delta_volume_value == -1:
                delta_volume_value = self.__volume_delta
            new_volume_value = min(100, current_volume + delta_volume_value)
            if new_volume_value == 100:
                self.__mediator.reproduce_speech(f"Громкость звука будет повышена до ста")
            self.set_volume(new_volume_value)
            if new_volume_value != 100:
                self.__mediator.reproduce_speech(f"Громкость звука повышена на {delta_volume_value}")

        elif command == VolumeCommands.down:
            current_volume = self.get_volume()
            delta_volume_value = self.__get_volume_value(command_string)
            if delta_volume_value == -1:
                delta_volume_value = self.__volume_delta
            new_volume_value = max(0, current_volume - delta_volume_value)
            if new_volume_value == 0:
                self.__mediator.reproduce_speech(f"Громкость звука будет понижена до нуля")
            self.set_volume(new_volume_value)
            if new_volume_value != 0:
                self.__mediator.reproduce_speech(f"Громкость звука понижена на {delta_volume_value}")

        elif command == VolumeCommands.failure:
            self.__mediator.reproduce_speech("К сожалению, я не понимаю такой команды настройки звука")

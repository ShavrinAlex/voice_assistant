from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from App.Recognizer.CommandRecognizer import CommandRecognizer
from App.Utils.Enums import VolumeCommands


COMMANDS_FILE = 'App/VolumeController/Commands.json'
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

    def __init__(self, volume_delta=10) -> None:
        self.__devices = AudioUtilities.GetSpeakers()
        self.__interface = self.__devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.__volume = self.__interface.QueryInterface(IAudioEndpointVolume)
        self.__cmd_recognizer = CommandRecognizer(VolumeCommands, COMMANDS_FILE, INDEX_OF_PROBABILITY)
        self.__volume_delta = volume_delta    # параметр на сколько увеличивать или уменьшать звук

    def __get_volume_value(self, command_string: str) -> int:
        try:
            return int(''.join(filter(str.isdigit, command_string)))
        except ValueError:
            return self.get_volume()

    def mute(self) -> None:
        self.__volume.SetMute(1, None)

    def unmute(self) -> None:
        self.__volume.SetMute(0, None)

    def get_volume(self) -> int:
        return int(self.__volume.GetMasterVolumeLevelScalar() * 100)

    def set_volume(self, volume_percentage: int) -> None:
        if volume_percentage < 0 or volume_percentage > 100:
            print('Incorrect volume value')
            return
        print(volume_percentage / 100)
        self.__volume.SetMasterVolumeLevelScalar(volume_percentage / 100, None)

    def execute(self, command_string: str) -> None:
        command = self.__cmd_recognizer.get_command(command_string)
        if command == VolumeCommands.set_value:
            volume_percentage = self.__get_volume_value(command_string)
            self.set_volume(volume_percentage)
        elif command == VolumeCommands.mute:
            self.mute()
        elif command == VolumeCommands.unmute:
            self.unmute()
        elif command == VolumeCommands.up:
            current_volume = self.get_volume()
            volume_value = self.__get_volume_value(command_string)
            if volume_value != current_volume:
                self.set_volume(min(100, current_volume + volume_value))
            else:
                self.set_volume(min(100, current_volume + self.__volume_delta))
        elif command == VolumeCommands.down:
            current_volume = self.get_volume()
            volume_value = self.__get_volume_value(command_string)
            if volume_value != current_volume:
                self.set_volume(max(0, current_volume - volume_value))
            else:
                self.set_volume(max(0, current_volume - self.__volume_delta))
        elif command == VolumeCommands.failure:
            print('Incorrect command')

'''
def main():
    sc = SoundController()
    while True:
        # Ввод процентного значения громкости от пользователя
        command = str(input("Введите команду: "))

        # Установка громкости
        sc.execute(command)
        print(sc.get_volume())



if __name__ == "__main__":
    main()
'''

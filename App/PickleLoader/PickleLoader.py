import pickle


class PickleLoader:
    """
    Класс Pickle загрузчика для сохранения данных приложения в двоичном виде и восстановления их обратно
    The Pickle class of the loader, for saving application data in binary form and restoring them back
    """

    @staticmethod
    def dump(data_to_dump: any, file_to_dump: str) -> None:
        """
        Функция непосредственной зарузки (сохранения) данных в файл
        The function of direct loading (saving) data to a file

        :param data_to_dump: any - любые данные для сохранения
        :param file_to_dump: string - путь к файлу сохранения (от корня проекта)

        :param data_to_dump: any - any data to dump
        :param file_to_dump: string - path to save file (from project root)
        """

        with open(file_to_dump, 'wb') as file:
            pickle.dump(data_to_dump, file)

    @staticmethod
    def load(file_to_load: str) -> any:
        """
        Функция непосредственной выгрузки данных из файла
        Function of direct unloading of data from a file

        :param file_to_load: string - путь к файлу восстановления (от корня проекта)
        :param file_to_load: string - path to the recovery file (from the project root)

        :return: any - любые данные, что были сохранены ранее
        :return: any - any data that was previously saved
        """

        with open(file_to_load, 'rb') as file:
            data = pickle.load(file)
        return data

import pickle


class PickleLoader:
    """
    Класс Pickle загрузчика для сохранения данных приложения в двоичном виде и восстановления их обратно
    The Pickle class of the loader, for saving application data in binary form and restoring them back
    """

    @staticmethod
    def dump(data_to_dump: list, file_to_dump: str) -> None:
        with open(file_to_dump, 'wb') as file:
            pickle.dump(data_to_dump, file)

    @staticmethod
    def load(file_to_load: str) -> list:
        with open(file_to_load, 'rb') as file:
            data = pickle.load(file)
        return data

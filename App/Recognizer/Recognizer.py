# машинное обучения для реализации возможности угадывания намерений
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

import json


# при добавлении новых команд стоит уменьшать этот показатель
#INDEX_OF_PROBABILITY = 0.5
#COMMANDS_FILE = 'App/Recognizer/GeneralCommands.json'


class Recognizer:
    """
    Класс распознавателя команд в тексте пользовательского запроса, который включает в себя следующие поля:
    The command recognizer class in the user request text, which includes the following fields:

    :field self.__vectorizer:
    :field self.__classifier_probability:
    :field self.__classifier:
    """

    def __init__(self, commands, commands_file: str, index_of_probability: float) -> None:
        self.commands = commands
        self.__commands_file = commands_file
        self.__index_of_probability = index_of_probability
        self.__vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
        self.__classifier_probability = LogisticRegression()
        self.__classifier = LinearSVC()
        self.prepare_corpus()

    def prepare_corpus(self) -> None:
        """"
        Подготовка модели для угадывания команды пользователя.
        This method prepares the model for guessing the user's command.
        """
        
        with open(self.__commands_file, encoding="UTF8") as file:
            config = json.load(file)

        corpus = []
        target_vector = []
        for intent_name, intent_data in config["commands"].items():
            for example in intent_data["examples"]:
                corpus.append(example)
                target_vector.append(intent_name)

        training_vector = self.__vectorizer.fit_transform(corpus)
        self.__classifier_probability.fit(training_vector, target_vector)
        self.__classifier.fit(training_vector, target_vector)

    def get_intent(self, user_request: str) -> any:
        """
        Функция преобразования запроса пользователя (user_request) в команду.
        This method converts a user request into a command.

        :params user_request: строка - формулировка запроса пользователя
        :params user_request: string - the wording of the user's request

        :return: наиболее вероятное "намерение" пользователя, либо None.
            кортеж вида (текстовая формулировка, коэффицент совпадения, 
            лучшее соответствие).
        :return: the most likely "intention" of the user, or None.
            a tuple of the form (textual formulation, coefficient of coincidence,
            best match).
        """
        
        best_intent = self.__classifier.predict(self.__vectorizer.transform([user_request]))[0]

        index_of_best_intent = list(self.__classifier_probability.classes_).index(best_intent)
        probabilities = self.__classifier_probability.predict_proba(self.__vectorizer.transform([user_request]))[0]

        best_intent_probability = probabilities[index_of_best_intent]

        if best_intent_probability > self.__index_of_probability:
            return user_request, best_intent_probability, best_intent

    def get_best_intent_in_list(self, intent_list: list):
        """
        Получение наиболее подходящей команды из списка соответствий.
        This method gets the most appropriate command from the list of matches.

        :params intent_list: список - все найденные соответствия
        :params intent_list: list - all matches found

        :return: Command - the element of listing all commands
        """

        if intent_list:
            intent_list.sort(key=lambda intent: intent[1])
            return self.commands[intent_list[-1][2]]
        return self.commands["failure"]
    
    @staticmethod
    def format_print_intent_list(intent_list: list) -> None:
        """
        Форматная печать всех соответствий с их коэфицентами совпадения.
        This function performs format printing of all matches with their matching coefficients.

        :params intent_list: список - все найденные соответствия
        :params intent_list: list - all matches found
        """

        if intent_list:
            intent_list.sort(key=lambda intent: intent[1])
            for request in intent_list:
                print('<-\t {:65} | {:20} | {}'.format(request[0], request[1], request[2]), '\n')
        else:
            print('<-\t No recognized intents')

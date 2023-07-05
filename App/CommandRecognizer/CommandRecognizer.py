# машинное обучения для реализации возможности угадывания намерений
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from App.Utils.Enums import Command
import json

# при добавлении новых команд стоит уменьшать этот показатель
INDEX_OF_PROBABILITY = 0.5
COMMANDS_FILE = 'App/CommandRecognizer/config.json'


class CommandRecognizer:
    """
    Класс распознавателя команд в тексте пользовательского запроса, который включает в себя следующие поля:
    The command recognizer class in the user request text, which includes the following fields:

    :field self.__vectorizer:
    :field self.__classifier_probability:
    :field self.__classifier:
    """

    def __init__(self) -> None:
        self.__vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
        self.__classifier_probability = LogisticRegression()
        self.__classifier = LinearSVC()
        self.prepare_corpus()

    def prepare_corpus(self) -> None:
        """"
        Подготовка модели для угадывания команды пользователя.
        This method prepares the model for guessing the user's command.
        """
        
        with open(COMMANDS_FILE, encoding="UTF8") as file:
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

        if best_intent_probability > INDEX_OF_PROBABILITY:
            return user_request, best_intent_probability, best_intent
    
    @staticmethod
    def get_best_intent_in_list(intent_list: list) -> Command:
        """
        Получение наиболее подходящей команды из списка соответствий.
        This method gets the most appropriate command from the list of matches.

        :params intent_list: список - все найденные соответствия
        :params intent_list: list - all matches found

        :return: Command - the element of listing all commands
        """

        if intent_list:
            intent_list.sort(key=lambda intent: intent[1])
            return Command[intent_list[-1][2]]
        return Command["failure"]
    
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

    def get_command(self, user_input: str) -> Command:
        """
        Поиск наилучшего соответствия.
        This method searches for the best match

        :params user_input: строка - пользовательский ввод, который необходимо 
            преобразовать к команде.
        :params user_input: string - user input that needs
            convert to command.

        :return: Command - the element of listing all commands
        """

        if user_input:
            text_parts = user_input.split()
            intent_list = []

            for lenght in range(len(text_parts)):
                for first_word in range(len(text_parts) - lenght):
                    final_word = first_word + lenght + 1

                    request = self.get_intent((" ".join(text_parts[first_word:final_word])).strip())
                    if request:
                        intent_list.append(request)

            intent_list.sort(key=lambda intent: intent[1])
            # self.format_print_intent_list(intent_list)

            best_intent = self.get_best_intent_in_list(intent_list)
            return best_intent
        else:
            return Command.failure

# машинное обучения для реализации возможности угадывания намерений
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from App.Utils.Enums import Command
import json

# при добавлении новых команд стоит уменьшать этот показатель
INDEX_OF_PROBABILITY = 0.5

class CommandRecognizer:
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
        self.classifier_probability = LogisticRegression()
        self.classifier = LinearSVC()
        self.prepare_corpus()

    def prepare_corpus(self) -> None:
        '''
        Подготовка модели для угадывания команды пользователя.
        '''
        
        with open('App/CommandRecognizer/config.json', encoding="UTF8") as file:
            config = json.load(file)

        corpus = []
        target_vector = []
        for intent_name, intent_data in config["commands"].items():
            for example in intent_data["examples"]:
                corpus.append(example)
                target_vector.append(intent_name)

        training_vector = self.vectorizer.fit_transform(corpus)
        self.classifier_probability.fit(training_vector, target_vector)
        self.classifier.fit(training_vector, target_vector)

    def get_intent(self, user_request) -> any:
        '''
        Функция преобразования запроса пользователя (user_request) в команду.
        :params user_request: строка - формулировка запрос пользователя
        :return: наиболее вероятное "намерение" пользователя, либо None.
            кортеж вида (текстовая формулировка, коэффицент совпадения, 
            лучшее соответствие).
        '''
        
        best_intent = self.classifier.predict(self.vectorizer.transform([user_request]))[0]

        index_of_best_intent = list(self.classifier_probability.classes_).index(best_intent)
        probabilities = self.classifier_probability.predict_proba(self.vectorizer.transform([user_request]))[0]

        best_intent_probability = probabilities[index_of_best_intent]

        if best_intent_probability > INDEX_OF_PROBABILITY:
            return user_request, best_intent_probability, best_intent
    
    @staticmethod
    def get_best_intent_in_list(intent_list) -> Command:
        '''
        Получение наиболее подходящей команды из списка соответствий.
        :params intent_list: список - все найденные соответствия
        :return:
        '''
        if intent_list:
            intent_list.sort(key=lambda intent: intent[1])
            return Command[intent_list[-1][2]]
        return Command["failure"]
    
    @staticmethod
    def format_print_intent_list(intent_list):
        '''
        Форматная печать всех соответствий с их коэфицентами совпадения.
        :params intent_list: список - все найденные соответствия
        :return:
        '''
        if intent_list:
            intent_list.sort(key=lambda intent: intent[1])
            for request in intent_list:
                print('<-\t {:65} | {:20} | {}'.format(request[0], request[1], request[2]), '\n')
        else:
            print('<-\t No recognized intents')

    def get_command(self, user_input) -> Command:
        '''
        Поиск наилучшего соответствия.
        :params user_input: строка - пользовательский ввод, который необходимо 
            преобразовать к команде.
        :return:
        '''
        if user_input:
            text_parts = user_input.split()
            intent_list = []

            for lenght in range(len(text_parts)):
                for first_word in range(len(text_parts) - lenght):
                    final_word = first_word + lenght + 1

                    request = self.get_intent((" ".join(text_parts[first_word:final_word])).strip())
                    if request != None:
                        intent_list.append(request)

            intent_list.sort(key=lambda intent: intent[1])
            # self.format_print_intent_list(intent_list)

            best_intent = self.get_best_intent_in_list(intent_list)
            return best_intent
        else:
            return Command.failure

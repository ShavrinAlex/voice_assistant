# машинное обучения для реализации возможности распознавания даты
# machine learning to implement date recognition capability
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from App.Utils.Enums import DateCommands
from App.VoiceAssistant import VoiceAssistant
from datetime import datetime, timedelta
import pickle
import json


# при добавлении новых команд стоит уменьшать этот показатель
INDEX_OF_PROBABILITY = 0
DATA_FILE = "App/AssistantFunctions/Reminder/config.json"
EVENT_STORAGE = "App/AssistantFunctions/Reminder/storage.pkl"


class Reminder:
    def __init__(self, mediator: VoiceAssistant):
        self.__mediator = mediator
        self.__vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
        self.__classifier_probability = LogisticRegression()
        self.__classifier = LinearSVC()
        self.prepare_corpus()

    def prepare_corpus(self) -> None:
        """
        Подготовка модели для распознавания даты.
        """
        with open(DATA_FILE, encoding="UTF8") as file:
            config = json.load(file)

        corpus = []
        target_vector = []
        for intent_name, intent_data in config["date"].items():
            for example in intent_data["examples"]:
                corpus.append(example)
                target_vector.append(intent_name)

        training_vector = self.__vectorizer.fit_transform(corpus)
        self.__classifier_probability.fit(training_vector, target_vector)
        self.__classifier.fit(training_vector, target_vector)

    def get_intent(self, request: str) -> any:
        """
        Функция преобразования запроса (request) в дату.
        :params user_request: строка - формулировка запрос пользователя
        :return: наиболее вероятное "намерение" пользователя, либо None.
            кортеж вида (текстовая формулировка, коэффицент совпадения, 
            лучшее соответствие).
        """
        
        best_intent = self.__classifier.predict(self.__vectorizer.transform([request]))[0]

        index_of_best_intent = list(self.__classifier_probability.classes_).index(best_intent)
        probabilities = self.__classifier_probability.predict_proba(self.__vectorizer.transform([request]))[0]

        best_intent_probability = probabilities[index_of_best_intent]

        if best_intent_probability > INDEX_OF_PROBABILITY:
            return request, best_intent_probability, best_intent
    
    @staticmethod
    def get_best_intent_in_list(intent_list: list):
        """
        Получение наиболее подходящей команды из списка соответствий.
        :params intent_list: список - все найденные соответствия
        :return:
        """
        if intent_list:
            intent_list.sort(key=lambda intent: intent[1])
            return DateCommands[intent_list[-1][2]].value
        return None

    @staticmethod
    def format_print_intent_list(intent_list: list) -> None:
        """
        Эта функция осуществляет форматную печать всех соответствий с их коэфицентами совпадения.
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

    def get_date(self, request: str) -> datetime:
        """
        Поиск наилучшего соответствия.
        :params user_input: строка, которую необходимо преобразовать к дате.
        :return:
        """
        event_date = datetime.today()
        if request:
            text_parts = request.split()
            intent_list = []
            for word in text_parts:
                intent_list.append(self.get_intent(word))
            self.format_print_intent_list(intent_list)
            
            change_date = self.get_best_intent_in_list(intent_list)
            print("change date", change_date)
            event_date = self.switch_change_date(event_date, change_date, self.recognize_num(request))         
            
        return event_date
    
    @staticmethod
    def switch_change_date(event_date: datetime, change_date: int, recognized_nums: list) -> datetime:
        new_date = event_date
        print("recognized nums", recognized_nums)
        # Месяц
        if change_date in range(1, 13):    
            print("in switch") 
            day = datetime.today().day
            month = change_date
            year = datetime.today().year
            if recognized_nums:
                for num in recognized_nums:
                    if num in range(1, 32):
                        day = num
                    elif num > year:
                        year = num
            new_date = datetime(year=year, month=month, day=day)
        # Завтра
        elif change_date == 14:             
            new_date = new_date + timedelta(days=1)
        # Послезавтра
        elif change_date == 15:             
            new_date = new_date + timedelta(days=2)
        # День недели
        elif change_date in range(20, 27):  
            weekday = change_date % 10
            new_date = new_date + timedelta(days=1)
            while new_date.weekday() != weekday:
                new_date = new_date + timedelta(days=1)
        return new_date
        
    @staticmethod
    def recognize_num(request: str) -> list:
        num_list = []
        text = request.split()
        for word in text:
            try:
                num_list.append(int(word))
            except:
                pass
        return num_list


    def create_promt(self) -> None:
        event_description = "$Unrecognized event$"
        event_date = None
        event_when_remind = 5

        while event_description == "$Unrecognized event$":
            self.__mediator.reproduce_speech("Запускаю процесс создания напоминания. Назовите событие.")
            event_description = self.__mediator.get_request()

        self.__mediator.reproduce_speech("Назовите дату.")
        user_response = self.__mediator.get_request()
        event_date = self.get_date(user_response)

        self.__mediator.reproduce_speech("За сколько дней до события начать напоминать?")
        user_response = self.__mediator.get_request()
        if len(self.recognize_num(user_response)):
            event_when_remind = self.recognize_num(user_response)[0]
        
        event_storage = None
        with open(EVENT_STORAGE, 'rb') as read_file:
            try:
                event_storage = pickle.load(read_file)
                if not event_storage:
                    event_storage = dict()
                event_storage[event_description] = {"remind_from": event_date - timedelta(days=event_when_remind), 
                                                    "remind_until": event_date,
                                                    "remind_range": event_when_remind}
            except:
                pass
        
        with open(EVENT_STORAGE, 'wb') as write_file:
            pickle.dump(event_storage, write_file)
        
        self.__mediator.reproduce_speech("создано напоминание " + event_description + " на " + event_date.strftime("%d %B %Y, %A"))
        print("напоминание", event_description, " на ", event_date.strftime("%d %B %Y, %A"))

from App.Utils.Enums import DateCommands
from App.AssistantFunctions.Reminder.ReminderDateRecognizer import ReminderDateRecognizer
from App.VoiceAssistant import VoiceAssistant
from datetime import datetime, timedelta
import pickle


# при добавлении новых команд стоит уменьшать этот показатель
INDEX_OF_PROBABILITY = 0
DATA_FILE = "App/AssistantFunctions/Reminder/config.json"
EVENT_STORAGE = "App/AssistantFunctions/Reminder/storage.pkl"


class Reminder:
    def __init__(self, mediator: VoiceAssistant) -> None:
        self.__mediator = mediator
        self.__recognizer = ReminderDateRecognizer(DateCommands, DATA_FILE, INDEX_OF_PROBABILITY)

    def create_promt(self) -> None:
        event_description = "$Unrecognized event$"
        event_date = None
        event_when_remind = 5

        while event_description == "$Unrecognized event$":
            self.__mediator.reproduce_speech("Запускаю процесс создания напоминания. Назовите событие.")
            event_description = self.__mediator.get_request()

        self.__mediator.reproduce_speech("Назовите дату.")
        user_response = self.__mediator.get_request()
        event_date = self.__recognizer.get_date(user_response)

        self.__mediator.reproduce_speech("За сколько дней до события начать напоминать?")
        user_response = self.__mediator.get_request()
        if len(self.__recognizer.recognize_num(user_response)):
            event_when_remind = self.__recognizer.recognize_num(user_response)[0]
        
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
        # print("напоминание", event_description, "на", event_date.strftime("%d %B %Y, %A"), "создано")

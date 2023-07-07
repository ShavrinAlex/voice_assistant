from datetime import datetime, timedelta
from App.AssistantFunctions.Reminder.ReminderWindow import ReminderWindow
import pickle


EVENT_STORAGE = "App/AssistantFunctions/Reminder/storage.pkl"


class ReminderChecker:
    def __init__(self):
        self.__notify_list = []

    def check_events(self):
        events_to_delete = []
        with open(EVENT_STORAGE, 'rb') as read_file:
            try:
                event_storage = pickle.load(read_file)
                if not event_storage:
                    event_storage = dict()
                for key in event_storage.keys():
                    if event_storage[key]["remind_from"] <= datetime.today():
                        self.notify(key, event_storage[key])
                    elif event_storage[key]["remind_until"] <= datetime.today():
                        events_to_delete.append(key)
                
                reminds_outputer = ReminderWindow(self.__notify_list)
                reminds_outputer.mainloop()

                for event in events_to_delete:
                    del(event_storage[event])
                    # pass
            except:
                pass
        with open(EVENT_STORAGE, 'wb') as write_file:
            pickle.dump(event_storage, write_file)
    
    def notify(self, promt_text: str, promt_data: dict):
        self.__notify_list.append([promt_text, promt_data["remind_until"].strftime("%d %m %Y"), promt_data["remind_range"]])
        # print("NOTIFY:", promt_text, promt_data["remind_until"].strftime("%d %m %Y"), "days:", promt_data["remind_range"])
from App.Recognizer.Recognizer import Recognizer
from datetime import datetime, timedelta

class ReminderDateRecognizer(Recognizer):
    def __init__(self, commands, commands_file: str, index_of_probability: float) -> None:
        super().__init__(commands, commands_file, index_of_probability)

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
            # self.format_print_intent_list(intent_list)
            
            change_date = self.get_best_intent_in_list(intent_list)
            event_date = self.switch_change_date(event_date, change_date, self.recognize_num(request))         
            
        return event_date
    
    def switch_change_date(self, event_date: datetime, change_date: int, recognized_nums: list) -> datetime:
        new_date = event_date
        # Месяц
        if change_date in range(1, 13):
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
        # 
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

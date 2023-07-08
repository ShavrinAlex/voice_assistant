import tkinter as tk
import tkinter.messagebox as mb

class ReminderWindow(tk.Tk):
    def __init__(self, events_to_remind: list):
        self.__remind_title = "Напоминание"
        self.__window_title = "Новое уведовмление!"
        super().__init__()
        btn_info = tk.Button(self, text=self.__window_title, command= lambda: 
                                self.open_reminds(events_to_remind))
        opts = {'padx': 40, 'pady': 5, 'expand': True, 'fill': tk.BOTH}
        btn_info.pack(**opts)
        pass

    def open_reminds(self, events_to_remind: list) -> None:
        for event in events_to_remind:
            event_message = event[0]
            event_date = event[1]
            event_remind_time = event[2]
            event_remind_time_for_output = "Напоминание за {} день".format(str(event_remind_time))
            output_string = "{} \n {} \n {}".format(event_message, event_date, event_remind_time_for_output)
            mb.showinfo(self.__remind_title, output_string)
        pass

if __name__ == "__main__":
    msg = "День рождение Васи"
    date = "7 июля"
    remind_time = 1
    window = ReminderWindow([[msg,date,remind_time], ["Уйти вечером в запой по заветам Рыбина", "7 июля", 2]])
    window.mainloop()
    pass

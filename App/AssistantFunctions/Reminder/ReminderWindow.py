import tkinter as tk
import tkinter.messagebox as mb


class ReminderWindow(tk.Tk):
    """
    Класс графического представления напоминаний
    Сlass of graphical representation of reminders
    """

    def __init__(self, events_to_remind: list) -> None:
        self.__remind_title = "Напоминание"
        self.__window_title = "Новое уведовмление!"
        super().__init__()
        btn_info = tk.Button(self, text=self.__window_title, command=lambda:self.open_reminds(events_to_remind))
        opts = {'padx': 40, 'pady': 5, 'expand': True, 'fill': tk.BOTH}
        btn_info.pack(**opts)

    def open_reminds(self, events_to_remind: list) -> None:
        """
        Метод, открывающий напоминание
        The method that opens the reminder

        :param events_to_remind: list - список событий для напоминания
        :param events_to_remind: list - list of events to remind
        """

        for event in events_to_remind:
            event_message = event[0]
            event_date = event[1]
            event_remind_time = event[2]
            event_remind_time_for_output = "Напоминание за {} день".format(str(event_remind_time))
            output_string = "{} \n {} \n {}".format(event_message, event_date, event_remind_time_for_output)
            mb.minsize(400, 80)
            mb.showinfo(self.__remind_title, output_string)

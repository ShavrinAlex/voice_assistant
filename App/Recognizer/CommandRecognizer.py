from App.Recognizer.Recognizer import Recognizer


class CommandRecognizer(Recognizer):
    """
    Класс распознование комманд пользователя для голосового ассистента
    Class for recognition of user commands for a voice assistant
    """

    def __init__(self, commands, commands_file: str, index_of_probability: float) -> None:
        super().__init__(commands, commands_file, index_of_probability)

    def get_command(self, user_input: str):
        """
        Этот метод осуществляет поиск наилучшего соответствия.
        This method searches for the best match.

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
            #self.format_print_intent_list(intent_list)

            best_intent = self.get_best_intent_in_list(intent_list)
            return best_intent
        else:
            return self.commands.failure

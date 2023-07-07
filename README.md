# voice_assistant

Rules:
1) Работаем под своей веткой с именем <ФамилияИмя>
2) Классы и файлы называем в *PascalCase*
3) Имя файла и папки по возможности совпадает с именем класса
4) Поля классов по возможности приватные <__поле_класса>
5) Переменные и методы называем в *snake_case*
6) Импорт библиотек от корневой <App...>
7) Комментарии по возможности на Английском
8) Изменение чужого кода только по согласованию
9) Комментарии должны быть максимально подробные <ФамилияИмя: перечисление всех нововведений>

# для запуска:
1. pip install pvporcupine
2. pip install pvrecorder
3. pip install PyAudio
4. pip install vosk
5. pip install pyttsx3
6. pip install SpeechRecognition
7. pip install scikit-learn
8. pip install translate
9. pip install screen_brightness_control
10. pip install pycaw

# Расширение функционала
Чтобы добавить свой функционал не забудьте:
1. В App.Utils.Enums.Command добавить соответствующую запись о своей команде;
2. В App.CommandRecognizer.config.json добавить запись о вашей команде, её номер Enum.Command и ключевые фразы для обучения распознавания;
3. Добавьте файлы вашей функции в отдельный каталог в App.AssistantFunctions;
4. Добавьте ваш функционал в App.CommandSwitcher.Switcher, по примеру других функций.

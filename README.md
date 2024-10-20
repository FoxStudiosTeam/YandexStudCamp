# Гойда_Танк ![GitHub top language](https://img.shields.io/github/languages/top/FoxStudiosTeam/YandexStudCamp?logo=python&logoColor=yellow) ![Коммиты](https://img.shields.io/github/commit-activity/t/FoxStudiosTeam/YandexStudCamp?logo=github&color=%2338f538) ![Пулл реквесты](https://img.shields.io/github/issues-pr-closed/FoxStudiosTeam/YandexStudCamp?logo=github)

Лучшее программное обеспечение для робота Xiao-r GFS-X, от Российских разработчиков в рамках участия в Студкемпе от Яндекс.

## Запуск робота
Для старта необходимо: 
1) Запустить файл [python_src/xr_startmain.py](https://github.com/FoxStudiosTeam/YandexStudCamp/blob/master/python_src/xr_startmain.py) на роботе.
2) На стороне сервера запустить файл [server-side/main.py](https://github.com/FoxStudiosTeam/YandexStudCamp/blob/master/server-side/main.py).
3) Ввести в консоль название цвета команды на английском языке.


## Структура проекта

### [camera-test](./camera-test)
Тестирование работы с камерами. Включает настройку нескольких камер. Предназначен для отладки и интеграции видеопотоков.

### [python_src](./python_src)
Основной код проекта. Включает клиентскую сторону проекта, распологается в роботе и предназначено для его управления и настройки.

### [server-side](./server-side)
Серверная часть проекта, которая отправляет команды на робота. Содержит финальные версии нейронных сетей, обработчики видео и модуль отправки команд на робота через tcp client.


## Используемые библиотеки

Проект использует следующие ключевые библиотеки:

1. **Ultralytics**  
   Фреймворк для работы с YOLOv8 (и другими версиями YOLO). Применяется для задач компьютерного зрения, таких как детекция объектов и их классификация.

2. **PyTorch**  
   Одна из ведущих библиотек для глубокого обучения. Используется для построения, обучения и развертывания нейросетей.

3. **Flask**  
   Лёгкий веб-фреймворк на Python, который используется для создания серверной части. Flask обеспечивает обработку HTTP-запросов и маршрутизацию.

4. **OpenCV**  
   Библиотека для обработки изображений и видео. В проекте используется для работы с видеопотоками и камерой, включая задачи обработки кадров и видеоанализ.
5. **EventBus**  
   Используется для организации и управления событиями в проекте. Обеспечивает подписку на события и передачу данных между модулями.

6. **NumPy**  
   Библиотека для работы с многомерными массивами и матричными операциями. Активно используется для обработки данных и выполнения вычислений, необходимых для тренировки нейросетей.

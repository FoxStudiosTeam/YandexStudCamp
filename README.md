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

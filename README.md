# Simple Voice Assistant

![GitHub License](https://img.shields.io/github/license/pentergust/simple-voice-assistant)

> Проект работает только в **Windows**.

Лет пять назад голосовые ассистенты из видео казались непостижимы.
И казалось что нельзя такого сделать самостоятельно.
Однако сейчас, имея нужжные технологии и знания можно с лёгкостью создать
своего собстенного голосового помошника.

Проект активно развивается.
Будем рады вашим идеям и предложениям с правками.
Милости просим к нам в [Telegram](https://t.me/iamlosethe).

## Установка и запуск

Клонируем репозиторий:
```sh
git clone https://github.com/Microvolna/simple-voice-assistant
```

Устанавливаем зависимости через *python venv*.
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Для запуска из *python venv*.
```sh
source venv/bin/activate
python main.py
```

## Возможности

- **Погода** -> Узнать погоду.
- **Время** -> отправляет текущее время.
- Открыть `калькулятор`.
- Открыть `cmd`.
- Как дела?.
- Привет.

### Погода

Написан небольшой парсер сайта [gismeteo](https://www.gismeteo.ru/).
Нахожу покзаателями этого сайта самыми точными.
Кстати, у gismeteo есть свой [API](https://www.gismeteo.ru/api/).

Для работы погоды измените в коде переменные `url` и `city` на свои.
```py
url = 'https://www.gismeteo.ru/weather-moscow-4368/'
city = 'в Москве'
```

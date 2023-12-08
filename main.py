"""
Simple voice assistant

Простой скрипт голосового ассистента.

Возможности
===========

- Привет => текст
- Погода => парсер gismeteo
- Как жизнь => текст
- Время => time
- Калькулятор => запуск приложения
- Коммнадная => запуск приложения

Author: Microvolna
Ver: 1.1
"""

from gtts import gTTS
import os
import time

import requests
from bs4 import BeautifulSoup
import speech_recognition as sr


# Замените на ссылку на gismeteo вашего города
url = 'https://www.gismeteo.ru/weather-moscow-4368/' 
# Замените на название вашего города в подобной форме
city = 'в Москве'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.2471 YaBrowser/23.11.0.2471 Yowser/2.5 Safari/537.36'
}


def main() -> None:
    r = sr.Recognizer()
    audio_response = None

    # Основной цикл программы
    while True:
        # Получаем звук с микрофона
        with sr.Microphone() as source:
            print("Cлушаю, господин")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        # Звук в текст
        try:
            text = r.recognize_google(audio, language="ru-RU")
            print("Вы сказали: " + text)
        except sr.UnknownValueError:
            audio_response = 'Извините, не удалось распознать речь'
        except sr.RequestError as e:
            audio_response = 'Ошибка сервиса распознавания речи'


        # Обработка текстовых запросов
        # ============================

        if 'привет' in str(text).lower() or 'здравствуйте' in str(text).lower() or 'здравствуй' in str(text).lower():
            audio_response = 'Здравствуйте, господин'

        elif 'погода' in str(text).lower() or 'погоду' in str(text).lower() or 'погоде' in str(text).lower() or 'температура' in str(text).lower() or 'температуре' in str(text).lower():
            response = requests.get(url, headers=headers)
            html = response.content

            soup = BeautifulSoup(html, 'html.parser')
            soup.html.body

            timing=soup.find('div', attrs={'class':'day'})
            temp=soup.find('span', attrs={'class':'unit unit_temperature_c'})
            temp_tomorrow_day=soup.find('span', attrs={'class':'unit unit_temperature_f'})

            if '−' in temp.text or '−' in temp_tomorrow_day.text:
                temp = "".join(filter(str.isdigit, temp.text))
                temp_tomorrow_day = "".join(filter(str.isdigit, temp_tomorrow_day.text))

                temp_minus = 'минус'
                temp_tomorrow_day_minus = 'минус'

                if int(temp) == int(temp_tomorrow_day):
                    raznitsa = 'также'
                elif int(temp) < int(temp_tomorrow_day):
                    raznitsa = 'холоднее'
                elif int(temp) > int(temp_tomorrow_day):
                    raznitsa = 'теплее'
            else:
                temp = temp.text
                temp_tomorrow_day = temp_tomorrow_day.text

                temp_minus = ''
                temp_tomorrow_day_minus = ''

                if int(temp) == int(temp_tomorrow_day):
                    raznitsa = 'также'
                elif int(temp) > int(temp_tomorrow_day):
                    raznitsa = 'холоднее'
                elif int(temp) < int(temp_tomorrow_day):
                    raznitsa = 'теплее'

            audio_response=f'По данным от гидрометеоцентра Гисметео на {timing.text} сегодня {city} {temp_minus} {temp} градуса по цельсию, а завтра днем будет {raznitsa} - {temp_tomorrow_day_minus} {temp_tomorrow_day} градуса по цельсию'

        elif 'как жизнь' in str(text).lower() or 'как дела' in str(text).lower() or 'как здоровье' in str(text).lower():
            audio_response = 'Да по тихоньку, по легоньку, а у вас как?'

        elif 'время' in str(text).lower() or 'времени' in str(text).lower() or 'который час' in str(text).lower():
            t = time.localtime()
            audio_response = f'Сейчас {time.strftime("%H часов %M минут и %S секунд", t)}, а это значит самое время идти с мамой куда-то'

        elif 'калькулятор' in str(text).lower() or 'посчитай' in str(text).lower() or 'сосчитай' in str(text).lower():
            audio_response = 'К сожалению у меня есть только его старая весия))'
            os.system('start calc.exe')

        elif 'коммандная' in str(text).lower() or 'строка' in str(text).lower() or 'взлом' in str(text).lower():
            audio_response = 'К сожалению у меня есть только его старая весия))'
            os.system('start cmd.exe')

        else:
            audio_response = 'Я вас не совсем пониаю, господин'

        try:
            print(audio_response)
            audio = gTTS(text=audio_response, lang='ru', slow=False)
            audio.save("example.mp3")
            os.system("start example.mp3")
        except:
            print('Проблемы с озвучкой')


# Запуск ассистента
# =================

if __name__ == "__main__":
    main()

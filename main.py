import speech_recognition as sr
from gtts import gTTS
import os
import time
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import g4f 
import consts


a = 1
while a != 0:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Cлушаю, '+consts.name)
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

        response = ''

    try:
        text = r.recognize_google(audio, language="ru-RU")
    except sr.UnknownValueError:
        response = 'Извините, не удалось распознать речь'
    except sr.RequestError as e:
        response = 'Ошибка сервиса распознавания речи'

    if response == '':
        if 'привет' in str(text).lower() or 'здравствуйте' in str(text).lower() or 'здравствуй' in str(text).lower():
            response = 'Здравствуйте, '+consts.name

        elif 'погода' in str(text).lower() or 'погоду' in str(text).lower() or 'погоде' in str(text).lower() or 'температура' in str(text).lower() or 'температуре' in str(text).lower():

            url = 'https://api.openweathermap.org/data/2.5/weather?q='+consts.city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

            weather_data = requests.get(url).json()

            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main'] ['feels_like'])

            response = 'Сейчас в '+consts.city+' '+str(temperature)+'°C, это ощущается как '+str(temperature_feels)+'°C'
            
        elif 'как жизнь' in str(text).lower() or 'как дела' in str(text).lower() or 'как здоровье' in str(text).lower():
            response = 'Да по тихоньку, по легоньку, а у вас как?'


        elif 'время' in str(text).lower() or 'времени' in str(text).lower() or 'который час' in str(text).lower():
            t = time.localtime()
            response = f'Сейчас {time.strftime("%H часов %M минут и %S секунд", t)}, а это значит самое время для подвигов'

        elif 'калькулятор' in str(text).lower() or 'посчитай' in str(text).lower() or 'сосчитай' in str(text).lower():
            response = 'Секунду'
            os.system('start calc.exe')

        elif 'коммандная' in str(text).lower() or 'строка' in str(text).lower() or 'взлом' in str(text).lower():
            response = 'Секунду'
            os.system('start cmd.exe')


        else:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f'Меня зовут - {consts.name}. Пожалуйста ответь на мой вопрос на русском языке: {text}'}],
                stream=False,
            )

            response = response.replace('GPT-3.5: ','')



    
        try:
            print(response)
            audio = gTTS(text=response, lang='ru', slow=False)
            audio.save('example.mp3')  
            playsound(os.getcwd() + '\example.mp3')
            response = ''
        except:
            print(f'Проблемы с озвучкой')

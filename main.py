import speech_recognition as sr
from gtts import gTTS
import os
import time
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import g4f 

url = 'https://www.gismeteo.ru/weather-moscow-4368/' # Замените на ссылку на gismeteo вашего города
city = 'в Москве' # Замените на название вашего города в подобной форме

a = 1
while a != 0:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Cлушаю, господин")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

        response = ''

    try:
        text = r.recognize_google(audio, language="ru-RU")
        print("Вы сказали: " + text)
    except sr.UnknownValueError:
        response = 'Извините, не удалось распознать речь'
    except sr.RequestError as e:
        response = 'Ошибка сервиса распознавания речи'

    if response == '':
        if 'привет' in str(text).lower() or 'здравствуйте' in str(text).lower() or 'здравствуй' in str(text).lower():
            response = 'Здравствуйте, господин'

        elif 'погода' in str(text).lower() or 'погоду' in str(text).lower() or 'погоде' in str(text).lower() or 'температура' in str(text).lower() or 'температуре' in str(text).lower():
            
            response = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.2471 YaBrowser/23.11.0.2471 Yowser/2.5 Safari/537.36'})
            html = response.content

            soup = BeautifulSoup(html, 'html.parser')
            
            geo = soup.find('h1')

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

            response=f'По данным от гидрометеоцентра Гисметео на {timing.text} сегодня {city} {temp_minus} {temp} градуса по цельсию, а завтра днем будет {raznitsa} - {temp_tomorrow_day_minus} {temp_tomorrow_day} градуса по цельсию'

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
                messages=[{"role": "user", "content": text}],
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

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.bot_app.models import *
from apps.stickers.models import Generate_Stickers, StikerPackConfig, Stiker_target_photo, Stiker_output_photo
from apps.bot_app.models import TelegramBotConfig, BotUser, GenerationProcess, Images, PromptModelSettings
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from django.http import HttpResponse
import requests
import json
import requests
import io
from PIL import Image
import time


def get_bot_token():
    config = TelegramBotConfig.objects.first()
    if config:
        return config.bot_token
    raise ValueError("Bot token not found in database")


class Task_Handler():
    def __init__(self) -> None:
        # self.bot = telebot.TeleBot(get_bot_token())
        pass




    def error_generations(self, task):
        print('Отправка пользователю')
        try:
            url = 'http://91.218.245.239:9999/task_error_alert'
            
            data = {
                "chat_id": task.user_id,
            }
            response = requests.post(url, data=data)
            print(response.json())
          
        except Exception as e:
            print('Ошибка в error_generations', e)







    def task_end_alert(self, task):
        print('Отправка пользователю')

        if task.target_photo == None:

            try:
                promt = PromptModelSettings.objects.get(men_promt=task.prompt)
            except:
                promt = PromptModelSettings.objects.get(women_promt=task.prompt)

            # Ожидаем пока появится path_on_tahe_photo, но с ограничением по времени/числу итераций


            while task.is_alert_sent == None:
                task.refresh_from_db()
                time.sleep(0.1)  # ждем секунду 

            # Проверяем результат ожидания
            if task.is_alert_sent == False:
                caption = f"Prompt id: {promt.number}\n\n{task.textovka_new}\n\n<b><a href='https://bcs.ru/?utm_source=bcs&utm_medium=tg_bot&utm_campaign=2bonus'>Узнай все про инвестиции с БКС Мир Инвестиций</a></b>\n\n{task.path_on_tahe_photo}"
                url = 'http://91.218.245.239:9999/task_complete_alert'
                # Отправка запроса
                task.is_alert_sent = True
                task.save()
                # Получение байтового содержимого файла
                with open(task.output_photo.image.path, 'rb') as file:
                    file_bytes = file.read()

                # Открытие изображения
                image = Image.open(io.BytesIO(file_bytes))

                # Загрузка логотипа
                logo = Image.open('/root/project/balancer-v2.0/face_to_face_server0/BCS_Logo.png')
                # logo = Image.open('/root/project/balancer-v2.0/face_to_face_server0/BCS-MI_Logo_RUS_CMYK.png')

                # Определение размера логотипа (можно настроить)
                logo_size = (550, 150)
                logo = logo.resize(logo_size)

                logo_padding_top = 40  # Отступ сверху
                x = image.size[0] - logo_size[0]  # Лого будет прижато к правому краю
                y = logo_padding_top
                image.paste(logo, (x, y), logo)
                # Сохранение изображения с логотипом
                output_path = task.output_photo.image.path
                image.save(output_path)

                # Получение байтового содержимого файла
                with open(task.output_photo.image.path, 'rb') as file:
                    new_file_bytes = file.read()

                print(f'Изображение с логотипом сохранено: {output_path}')
                
                # # Создание объекта BytesIO
                # byte_file = io.BytesIO(file_bytes)
                byte_file = io.BytesIO(new_file_bytes)
                byte_file.name = f'image_{task.id}.jpg'  # Укажите имя файла для передачи
                
                # Подготовка данных для отправки
                files = {'photo': (f'image_{task.id}.jpg', byte_file, 'image/jpeg')}  # image/jpeg — MIME-тип
                data = {
                    "chat_id": task.user_id,
                    "caption": caption,
                    "target_photo_status": "False",
                    "task_id": task.id,
                    "path_on_the_photo": task.path_on_tahe_photo,
                }

                try:
                    response = requests.post(url, data=data, files=files)
                    response.raise_for_status()
                    print(response.json())
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка отправки запроса: {e}")




        if task.target_photo != None:
            caption = f"{task.textovka_new}\n\n<b><a href='https://bcs.ru/?utm_source=bcs&utm_medium=tg_bot&utm_campaign=2bonus'>Узнай все про инвестиции с БКС Мир Инвестиций</a></b>"
            url = 'http://91.218.245.239:9999/task_complete_alert'
            
            # Получение байтового содержимого файла
            with open(task.output_photo.image.path, 'rb') as file:
                file_bytes = file.read()

            # Открытие изображения
            image = Image.open(io.BytesIO(file_bytes))

            # Загрузка логотипа
            logo = Image.open('/root/project/balancer-v2.0/face_to_face_server0/BCS_Logo.png')
            # logo = Image.open('/root/project/balancer-v2.0/face_to_face_server0/BCS-MI_Logo_RUS_CMYK.png')

            # Определение размера логотипа (можно настроить)
            logo_size = (550, 150)
            logo = logo.resize(logo_size)

            logo_padding_top = 40  # Отступ сверху
            x = image.size[0] - logo_size[0]  # Лого будет прижато к правому краю
            y = logo_padding_top
            image.paste(logo, (x, y), logo)
            # Сохранение изображения с логотипом
            output_path = task.output_photo.image.path
            image.save(output_path)

            # Получение байтового содержимого файла
            with open(task.output_photo.image.path, 'rb') as file:
                new_file_bytes = file.read()

            print(f'Изображение с логотипом сохранено: {output_path}')
            
            # Создание объекта BytesIO
            byte_file = io.BytesIO(new_file_bytes)
            # byte_file = io.BytesIO(file_bytes)
            byte_file.name = f'image_{task.id}.jpg'  # Укажите имя файла для передачи
            
            # Подготовка данных для отправки
            files = {'photo': (f'image_{task.id}.jpg', byte_file, 'image/jpeg')}  # image/jpeg — MIME-тип
            data = {
                "chat_id": task.user_id,
                "caption": caption,
                "target_photo_status": "True",
                "task_id": task.id,
                "path_on_the_photo": task.path_on_tahe_photo,
                
                
            }

            # Отправка запроса
            try:
                response = requests.post(url, data=data, files=files)
                response.raise_for_status()
                print(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Ошибка отправки запроса: {e}")





# from apps.bot_app.models import GenerationProcess
# def task_end_alert(task):
#     print('Сохранение изображения с логотипом')

#     # Получение байтового содержимого файла
#     with open(task.output_photo.image.path, 'rb') as file:
#         file_bytes = file.read()

#     # Открытие изображения
#     image = Image.open(io.BytesIO(file_bytes))

#     # Загрузка логотипа
#     logo = Image.open('/root/project/balancer-v2.0/face_to_face_server0/BCS_Logo.png')

#     # Определение размера логотипа (можно настроить)
#     logo_size = (100, 100)
#     logo = logo.resize(logo_size)

#     # Расположение логотипа на изображении (можно настроить)
#     x, y = image.size[0] - logo_size[0] - 20, image.size[1] - logo_size[1] - 20
#     image.paste(logo, (x, y), logo)

#     # Сохранение изображения с логотипом
#     output_path = f'output/image_{task.id}_with_logo.jpg'
#     image.save(output_path)

#     print(f'Изображение с логотипом сохранено: {output_path}')

# task = GenerationProcess.objects.get(id=3921)
# task_end_alert(task)
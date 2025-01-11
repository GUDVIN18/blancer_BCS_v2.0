import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_to_face_server0.settings')
django.setup()
from apps.bot_app.models import BotUser, GenerationProcess, LoggingProccess
import requests
import time


def main(users_all):
    for user in users_all:
        tg_id = user
        try:
            obj = LoggingProccess.objects.filter(user_id=tg_id).order_by('id').first()
            if obj:
                count_generation = LoggingProccess.objects.filter(user_id=tg_id).count()
                interes = obj.user_category
                gender = obj.gender
                time_invest = obj.time_invest
                investor_risk = obj.investor_risk
                user_price = obj.user_price
                data = {
                    "tg_id": obj.user_id,
                    "count_generation": count_generation,
                    "interes": interes,
                    "gender": gender,
                    "time_invest": time_invest,
                    "investor_risk": investor_risk,
                    "user_price": user_price,
                }
                print('Отправка')
                response = requests.post('http://91.218.245.239:9999/update_user_data', data=data)
                print(f"Статус ответа: {response.status_code}")
                print(f"Тело ответа: {response.text}")
                response_json = response.json()  # Проверка на JSON
                print("Ответ сервера:", response_json)

    
        except Exception as e:
            print('Лога нет', e)
            time.sleep(0.05)
            continue
        time.sleep(0.05)

if __name__ == '__main__':
    response = requests.get('https://bcs-invest-balanser.site/get_user_id_all', stream=True)

    print(f"Статус ответа: {response.status_code}")
    print(f"Тело ответа: {response.text}")

    try:
        users_all = response.json()
        if 'users_id' in users_all:
            users_all = users_all['users_id']
            print("Получен список пользователей:", len(users_all))
    except ValueError as e:
        print("Некорректный JSON в ответе:", e)
    main(users_all)
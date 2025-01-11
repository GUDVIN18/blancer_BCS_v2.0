from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import logging
from apps.bot_app.models import GenerationProcess
import os
import random


def index(request):
    return render(request, "index.html")


def upload_photo(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        gender = request.POST.get('gender')
        style = request.POST.get('style')

        print('Успешно приняли данные',)
        # Получаем путь до текущего файла (без имени файла в конце)
        # current_file_path = os.path.abspath(__file__)
        # base_dir = os.path.dirname(current_file_path)
        

        # Формируем путь в зависимости от пола
        if gender == "Man":
            gender = "male, man, masculine"
            
        if gender == "Woman":
            gender = "female, woman, feminine"

        if gender == "Two-Man":
            gender = "two males, 2 men, manly men"

        if gender == "Two-Woman":
            gender = "two females, 2 women, feminine women"

        if gender == "Man-Left-Woman-Right":
            gender = "male on left, female on right, man woman couple"

        if gender == "Woman-Left-Man-Right":
            gender = "female on left, male on right, woman man couple"

        # if style == "halloween":
        #     base_path += "/halloween"
        # if style == "astronaut":
        #     base_path += "/nasa"
        # if style == "christmas":
        #     base_path += "/new_year"
        # if style == "superhero":
        #     base_path += "/super_man"
        
        # # Получаем список всех файлов в папке
        # files = os.listdir(base_path)

        # Фильтруем только изображения (например, PNG, JPG)
        # image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # # Выбираем случайный файл
        # random_image = random.choice(image_files)

        # # Формируем полный путь
        # target_photo_path = os.path.join(base_path, random_image)



        if style == "halloween":
            prompt = f"A cinematic portrait of {gender}, aged **, in a detailed Gothic vampire costume, pale skin with soft freckles, sharp and symmetrical facial features, curly black hair cascading over her shoulders, intense green eyes, captured under dim candlelight. The background features a foggy Victorian cemetery with ornate tombstones, intricate wrought-iron gates, and a full moon casting a silver glow. Created using: Canon EOS-5D, chiaroscuro lighting, fine brush digital detailing, inspired by Baroque portraiture, hyper-realistic texture, hd quality, natural style --ar 2:3 --v 6.0"
        if style == "astronaut":
            prompt = f"A ** year-old {gender} stands in a NASA astronaut costume at the cosmodrome, without a helmet. The most detailed and realistic face"
        if style == "christmas":
            prompt = f"((gender: {gender}!)), ** years old, realistic portrait, wearing classic green christmas sweater and red pants, natural indoor setting, soft daylight, neutral facial expression, no smile, no headwear, sharp facial details, photorealistic quality"
        if style == "superhero":
            prompt = f"((gender: {gender}!)),  years old, dressed in a vibrant superhero costume with a striking red and blue suit, cape billowing dramatically in the wind. The superhero stands confidently in front of a city skyline, poised for action. The lighting is cinematic, enhancing the heroic aura surrounding them, with every muscle defined and perfectly detailed. The face is calm and focused, with a slight smile indicating confidence and determination. The face is super-realistic with high facial detail, capturing the essence of a true superhero, with no headgear, allowing the full expression of their facial features to shine through."


        # Подготовка данных для отправки на другой сервер
        files = {
            'user_photo': photo,
        }
        
        data = {
            'task_end_handler': 'task_end_alert',
            'prompt': prompt,
        }
        # Отправка данных на другой сервер (замените URL на нужный вам)
        response = requests.post('http://91.218.245.239:8091/create_task', files=files, data=data)
        # Parse the JSON response directly
        response_data = response.json()
        task_id = response_data.get("task_id")
        status = response_data.get("status")
        user_waiting = response_data.get("user_waiting")
            
    # Return the task_id as a JSON response
    return JsonResponse({'task_id': task_id, 'status':status, 'user_waiting':user_waiting})



logger = logging.getLogger(__name__)

@csrf_exempt
def task_complete_alert(request, task_id=None):
    try:
        if request.method == 'POST':
            # Use the task_id from the URL path if provided
            if task_id:
                try:
                    latest_photo = GenerationProcess.objects.get(id=task_id)
                    return JsonResponse({
                        'status': 'success',
                        'photo_url': latest_photo.output_photo.image.url
                    })
                except GenerationProcess.DoesNotExist:
                    return JsonResponse({
                        'status': 'loading',
                        'message': 'Photo is still generating...'
                    })
            
            return JsonResponse({
                'status': 'error',
                'message': 'No task_id provided'
            })
           
        # Handle GET requests for displaying the photo
        if task_id:
            try:
                latest_photo = GenerationProcess.objects.get(id=task_id)
                return render(request, 'check.html', {
                    'photo_url': latest_photo.output_photo.image.url
                })
            except GenerationProcess.DoesNotExist:
                return render(request, 'check.html', {'photo_url': None})
        
        return render(request, 'check.html', {'photo_url': None})
    
    except Exception as e:
        logger.error(f"Error in task_complete_alert: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

import requests
import time
import os
import django
import concurrent.futures
from PIL import Image
import io
import requests
from django.core.files import File

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_to_face_server0.settings')

# Configure Django
django.setup()
from apps.bot_app.models import PromptModelSettings, GenerationProcess, Images
import uuid
from django.core.files.base import ContentFile
import io



# Функция ожидания появления изображений
chat_id = -1002423543289


def wait_for_images(generation_id, headers):
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            generated_images = data.get("generations_by_pk", {}).get("generated_images", [])
            if generated_images:  # Проверяем, есть ли изображения
                return generated_images
        else:
            print(f"Ошибка при получении данных: {response.status_code}")
            return []
        time.sleep(2)  # Проверка каждые 1 секунду







# Функция для загрузки изображения
def load_image(file_path):
    """
    Safely load an image file with error handling and validation
    """
    try:
        with open(file_path, 'rb') as file:
            image_content = file.read()
            
        # Проверка, что это валидное изображение
        img = Image.open(io.BytesIO(image_content))
        img.verify()  # Проверка целостности изображения
        return ContentFile(image_content, name='uploaded_image.jpg')
    except (IOError, Image.UnidentifiedImageError) as e:
        print(f"Error loading or validating image {file_path}: {e}")
        return None



def download_image(image_url, save_path):
    """
    Download an image from a URL and save it locally
    """
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print(f"Фото успешно сохранено: {save_path}")
        return save_path
    else:
        print(f"Ошибка при скачивании изображения: {response.status_code}")
        return None



def leonardo_generations(prompt, negative_prompt, orientation, number_photo, gender, num_gen, file_path):
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    
    n_prompt = negative_prompt
    full_file_path = file_path

    #Тут еще и промты и orientation
    # user_photo_file = request.FILES.get("user_photo")

    textovka = "стать ... Тест через Leonardo! Без текстовки"
    summa = '1'
    period = "20"
    interes = "Эмоции / Вдохновение"
    type_investor = 'Консервативный'
    gender = 'Мужчина'
    # full_file_path = '/root/project/balancer-v2.0/face_to_face_server0/media/saha_tai.jpg'


    if orientation == "Вертикальный":


# url = "https://cloud.leonardo.ai/api/rest/v1/generations"

# payload = {
#     "alchemy": True,
#     "height": 1920,
#     "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",
#     "num_images": 4,
#     "presetStyle": "DYNAMIC",
#     "prompt": "A majestic cat in the snow",
#     "width": 1024,
#     "highContrast": False,
#     "highResolution": True,
#     "fantasyAvatar": False,
#     "contrastRatio": 0,
#     "negative_prompt": "Women",
#     
#     "photoRealStrength": 0.45,
#     "promptMagic": False,
#     "photoRealVersion": "v2"
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)

        # payload = {
        #     "alchemy": True,
        #     "height": 1360,
        #     "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",  # Убедитесь, что это ID поддерживаемой модели
        #     "num_images": number_photo,
        #     "presetStyle": "DYNAMIC",
        #     "prompt": prompt,
        #     "width": 768,
        #     "highContrast": False,
        #     "highResolution": True,
        #     "fantasyAvatar": False,
        #     "contrastRatio": 0,
        #     "negative_prompt": n_prompt,
        #     "photoReal": True,
        #     "photoRealVersion": "v2",
        #     "promptMagic": False,
        # }

        payload = {
            "alchemy": True,
            "height": 1360,
            "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",  # Убедитесь, что это ID поддерживаемой модели
            "num_images": number_photo,
            "presetStyle": "STOCK_PHOTO",
            "prompt": prompt,
            "width": 768,
            "highContrast": False,
            "highResolution": False,
            "fantasyAvatar": False,
            "contrastRatio": 0,
            "negative_prompt": n_prompt,
            # "photoReal": True,
            # "photoRealVersion": "v2",
            "promptMagic": False,
        }
    else:
        payload = {
            "alchemy": True,
            "height": 768,
            "modelId": "aa77f04e-3eec-4034-9c07-d0f619684628",
            "num_images": number_photo,
            "presetStyle": "STOCK_PHOTO",
            "prompt": prompt,
            "width": 1360,
            "highContrast": False,
            "highResolution": True,
            "fantasyAvatar": False,
            "contrastRatio": 0,
            "negative_prompt": n_prompt,
            "photoReal": True,
            "photoRealStrength": 0.45,
            "promptMagic": False,

        }


    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer e0a060d8-ac47-425b-a811-a9041d296cf5"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        generation_id = result['sdGenerationJob']['generationId']
        print(f"Запрос успешно отправлен. ID генерации: {generation_id}")
    else:
        print(f"Ошибка при отправке запроса: {response.status_code} - {response.text}")
        generation_id = None

    # Проверка и ожидание изображений
    if generation_id:
        print("Ожидание генерации изображений...")
        generated_images = wait_for_images(generation_id, headers)

        if generated_images:
            # Получаем URL всех изображений
            image_urls = [img.get("url") for img in generated_images if img.get("url")]
            for idx, image_url in enumerate(image_urls, start=1):
                print(f"Image {idx}: {image_url}")
                if orientation == "Вертикальный":
                    prompt_folder = f"/root/project/balancer-v2.0/face_to_face_server0/media/leonardo_kino_xl/{orientation}/"
                else:
                    prompt_folder = f"/root/project/balancer-v2.0/face_to_face_server0/media/leonardo_kino_xl/{orientation}/"

                filename = f"photo_{num_gen}_{idx}_{orientation.lower()}_{gender}.png"
                save_path = os.path.join(prompt_folder, filename)

                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    if response.status_code == 200:
                        download_image(image_url, save_path)
                        save_photo_saha = load_image(full_file_path)



                    time.sleep(2)
                    # with open(full_file_path, 'rb') as f:
                    #     # Создаем объект Images для photo
                    #     photo_object = Images.objects.create(
                    #         description='Исходное фото пользователя',
                    #         image=File(f, name='source_photo.jpg')
                    #     )
                    #     time.sleep(1)
                        # Создаем объект Images для target_photo

                    photo = Images.objects.create(
                        description='Саша',
                        image=save_photo_saha,
                    )

                    with open(save_path, 'rb') as f:
                        target_photo = Images.objects.create(
                            description='Фото на кого будет наложено',
                            image=File(f, name='leo.jpg')
                        )
                    new_generation = GenerationProcess(
                        textovka_new=textovka,
                        user_id=gender,
                        photo=photo,
                        target_photo=target_photo,  # Передаём объект File
                        format_photo=orientation,
                        process_status='WAITING',
                        process_backend_id=uuid.uuid4(),
                        task_end_handler='task_end_alert',
                    )
                    
                    new_generation.save()
            

            print('Все фото сохранены!\n\n')


            # men_input_image = '/root/project/balancer-v2.0/face_to_face_server0/media/saha_tai.jpg'
            # with open(men_input_image, 'rb') as file:
            #     files = {'user_photo': file}
            #     data = {
            #         'user_id': chat_id,
            #         'prompt': f"promt_user 250_3_Автомобили_{gender}_{orientation}",
            #         'format_photo': orientation,
            #         'task_end_handler': 'task_end_alert',
            #         'generation_or_face_to_face': 'False',
            #         'promt_num': prompt_number,
            #     }
            #     time.sleep(1)
            #     # Отправка задачи на создание
            #     response = requests.post('http://91.218.245.239:8091/create_task', data=data, files=files)
            #     time.sleep(2)
            #     task_info = response.json()
            #     print('task_info', task_info)


            task_id = int(new_generation.id)

                    
            while True:
                status_response = requests.get(f'http://91.218.245.239:8091/task_status/{task_id}')
                status_data = status_response.json()
                
                if status_data['status'] == 'COMPLETED':
                    file_response = requests.get(f'http://91.218.245.239:8091/get_file/{task_id}')
                    
                    if file_response.status_code != 200:
                        print(f'Не удалось получить файл. Статус-код: {file_response.status_code}')
                        return False

                    if len(file_response.content) == 0:
                        print(f'Полученный файл пуст для задачи {task_id}')
                        return False
                    
    
                    # Обновление записи в базе данных
                    try:
                        gen_process = GenerationProcess.objects.get(id=task_id)
                        
                        # Сохранение абсолютного пути 
                        gen_process.path_on_tahe_photo = f"ProccessId={gen_process.id}\n⬆️ Путь до фото: <code>{save_path}</code>"
                        gen_process.save()
                        
                        return True
                    
                    except GenerationProcess.DoesNotExist:
                        print(f'Не найдена запись GenerationProcess для задачи {task_id}')
                        return False

                
                elif status_data['status'] == 'ERROR_GENERATION':
                    print(f'Ошибка генерации фото: {status_data}')
                    return False
                
                time.sleep(5)





        return True

    else:
        print("Изображения не были сгенерированы.")
        return False







# if __name__ == '__main__':
    
#     prompts = list(PromptModelSettings.objects.all().order_by('id'))

#     prompt = 'Flawless anatomy, medium shot, medium normal height, white Slavic skin, soft face, a confident businesswoman with soft, rounded facial features, natural clean skin, and medium build, walking gracefully along a luxurious pier on the Riviera, surrounded by exclusive yachts. She exudes elegance and sophistication, dressed in a crisp, loose-fitting white linen shirt (untucked) paired with tailored high-waisted navy trousers and polished leather loafers, blending effortless style with an air of authority. Her arms hang naturally at her sides as she walks with purpose, looking directly into the camera with a calm, self-assured smile. The long, polished wooden pier stretches into the distance, flanked by sleek, high-end yachts reflecting the warm golden hues of the evening sunset. Subtle reflections of the yachts and pier shimmer softly on the clear blue water, adding depth and realism to the scene. The camera is positioned at shoulder height, capturing a balanced perspective of the woman and her luxurious surroundings. Ultra-realistic textures, cinematic lighting, natural muted colors, sharp 8K resolution, professional composition, clean details, no artifacts, and no other people visible.'
#     negative_prompt = "Overly close-up views, exaggerated or sharp facial features, angular or overly thin build, stiff or unnatural poses, casual or poorly fitted clothing, overly saturated colors, futuristic or sci-fi elements, cluttered or chaotic backgrounds, low resolution, artifacts, additional people, irrelevant objects, and unrealistic pier or yacht details."
#     orientation = "Вертикальный"
#     number_photo = 1
#     gender = 'men'
#     num_gen = 1
#     status_gen = leonardo_generations(prompt, negative_prompt, orientation, number_photo, gender, num_gen)

#     # if status_gen == True:
#     #     num_gen = 2
#     #     status_gen = main(prompt_men, negative_prompt, orientation, number_photo, gender, num_gen)
#     #     print(status_gen)



                

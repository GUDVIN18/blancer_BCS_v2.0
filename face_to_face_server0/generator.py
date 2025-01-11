import os
import django
import time
import requests
import concurrent.futures
from PIL import Image
import io

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_to_face_server0.settings')

# Configure Django
django.setup()
from apps.bot_app.models import PromptModelSettings, GenerationProcess
chat_id = -1002423543289

# Укажи номера промтов в БД
prompts_mas = list(range(1, 89))

#Кол-во фоток , которое нужно сделать
photo_count = 14

women = True
men = True




def load_image(file_path):
    """
    Safely load an image file with error handling and validation
    """
    try:
        with open(file_path, 'rb') as file:
            image_content = file.read()
            
        # Проверка, что это валидное изображение
        Image.open(io.BytesIO(image_content))
        return image_content
    except (IOError, Image.UnidentifiedImageError) as e:
        print(f"Error loading or validating image {file_path}: {e}")
        return None

def process_task(file_content, user_id, prompt, negative_prompt, format_photo, folder, gender, task_index):
    """
    Process a single photo generation task with improved error handling and path saving
    """
    try:
        # Подготовка данных для запроса
        files = {'user_photo': file_content}
        data = {
            'user_id': user_id,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'format_photo': format_photo,
            'task_end_handler': 'task_end_alert',
            'generation_or_face_to_face': 'True',
        }
        time.sleep(1.5)
        # Отправка задачи на создание
        response = requests.post('http://91.218.245.239:8091/create_task', data=data, files=files)
        task_info = response.json()
        print('task_info', task_info)
        time.sleep(1)
        
        # Проверка, что задача создана
        if 'task_id' not in task_info:
            print(f"Ошибка создания задачи: {task_info}")
            return False

        task_id = int(task_info["task_id"])
        
        # Ожидание завершения задачи
        while True:
            status_response = requests.get(f'http://91.218.245.239:8091/task_status/{task_id}')
            status_data = status_response.json()
            
            if status_data['status'] == 'COMPLETED':
                # Получение файла
                file_response = requests.get(f'http://91.218.245.239:8091/get_file/{task_id}')
                
                if file_response.status_code != 200:
                    print(f'Не удалось получить файл. Статус-код: {file_response.status_code}')
                    return False

                # Проверка содержимого файла
                if len(file_response.content) == 0:
                    print(f'Полученный файл пуст для задачи {task_id}')
                    return False

                # Формирование пути для сохранения
                gen_process = GenerationProcess.objects.get(id=task_id)
                new_filename = f'photo_{gen_process.format_photo.lower()}_{task_index}_{gender}_{gen_process.format_photo.lower()}.png'
                new_photo_path = os.path.join(folder, new_filename)
                
                try:
                    # Сохранение файла
                    with open(new_photo_path, 'wb') as f:
                        f.write(file_response.content)
                    
                    # Обновление записи в базе данных
                    try:
                        gen_process = GenerationProcess.objects.get(id=task_id)
                        
                        # Сохранение абсолютного пути 
                        gen_process.path_on_tahe_photo = f"ProccessId={gen_process.id}\n⬆️ Путь до фото: <code>{os.path.abspath(new_photo_path)}</code>"
                        gen_process.is_alert_sent = False
                        gen_process.save()
                        print(f'Файл успешно сохранен: {new_photo_path}')
                        print(f'Путь в базе данных: {gen_process.path_on_tahe_photo}')
                        
                        return True
                    
                    except GenerationProcess.DoesNotExist:
                        print(f'Не найдена запись GenerationProcess для задачи {task_id}')
                        return False
                    
                except (IOError, Image.UnidentifiedImageError) as img_error:
                    print(f'Ошибка при обработке изображения: {img_error}')
                    return False
            
            elif status_data['status'] == 'ERROR':
                print(f'Ошибка генерации фото: {status_data}')
                return False
            
            # Увеличим интервал ожидания
            time.sleep(5)
    
    except Exception as e:
        print(f"Критическая ошибка в process_task: {e}")
        return False





import random

def main(photo_count, men, women, orientations_1, orientations_2, men_input_image, women_input_image):
    # Get all prompts
    prompts = list(PromptModelSettings.objects.all().order_by('id'))
    user_id = chat_id

    # Load images once
    men_image_content = load_image(men_input_image)
    women_image_content = load_image(women_input_image)

    if men_image_content is None or women_image_content is None:
        print("Failed to load input images. Exiting.")
        return

    for promt in prompts:
        try:
            for promt_num in prompts_mas:
                if promt_num == promt.number:
                    print(f'Принят: promt.number {promt.number}\npromt_num {promt_num}\n')
                    # Create main folder for prompt
                    promt_folder = os.path.join('/root/project/balancer-v2.0/face_to_face_server0/media', str(f'{promt.number}_neiro1'))
                    os.makedirs(promt_folder, exist_ok=True)

                    men_folder = os.path.join(promt_folder, 'men')
                    women_folder = os.path.join(promt_folder, 'women')
                    os.makedirs(men_folder, exist_ok=True)
                    os.makedirs(women_folder, exist_ok=True)

                    if men:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=photo_count) as executor:
                            i = random.randint(1, 99999999999999999)
                            men_futures_1 = [
                                executor.submit(
                                    process_task, 
                                    men_image_content, 
                                    user_id, 
                                    promt.men_promt, 
                                    promt.negative_prompt,
                                    orientations_1,
                                    men_folder, 
                                    'men', 
                                    f'{orientations_1.lower()}_{i+j}'
                                ) for j in range(1, photo_count + 1)
                            ]

                            men_futures_2 = [
                                executor.submit(
                                    process_task, 
                                    men_image_content, 
                                    user_id, 
                                    promt.men_promt, 
                                    promt.negative_prompt,
                                    orientations_2,
                                    men_folder,
                                    'men',
                                    f'{orientations_2.lower()}_{i+j}'
                                ) for j in range(1, photo_count + 1)
                            ]
                            concurrent.futures.wait(men_futures_1 + men_futures_2)
                    if women:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=photo_count) as executor:
                            i = random.randint(1, 99999999999999999)
                            women_futures_1 = [
                                executor.submit(
                                    process_task, 
                                    women_image_content, 
                                    user_id, 
                                    promt.women_promt, 
                                    promt.negative_prompt,
                                    orientations_1,
                                    women_folder, 
                                    'women', 
                                    f'{orientations_1.lower()}_{i+j}'
                                ) for j in range(1, photo_count + 1)
                            ]

                            women_futures_2 = [
                                executor.submit(
                                    process_task, 
                                    women_image_content, 
                                    user_id, 
                                    promt.women_promt, 
                                    promt.negative_prompt,
                                    orientations_2,
                                    women_folder, 
                                    'women', 
                                    f'{orientations_2.lower()}_{i+j}'
                                ) for j in range(1, photo_count + 1)
                            ]
                        
                            concurrent.futures.wait(women_futures_1 + women_futures_2)
        except Exception as e:
            print('Промта не существует!', e)       

    print(f'Processed prompt {promt.number}')








orientations_1 = "Вертикальный"
orientations_2 = "Горизонтальный"

# n_input_image = '/root/project/balancer-v2.0/face_to_face_server0/media/50_generator/e61YZtCZdSb6T.jpeg'
men_input_image = '/root/project/balancer-v2.0/face_to_face_server0/media/saha_tai.jpg'
women_input_image = '/root/project/balancer-v2.0/face_to_face_server0/gggggggggggggggggggggggggg.jpg'

if __name__ == '__main__':
    main(photo_count, men, women, orientations_1, orientations_2, men_input_image, women_input_image)
    print('Успешное завершение')
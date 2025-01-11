# import os
# import shutil

# def distribute_zip_files(source_folder, destination_root):
#     # Создаем необходимые пути
#     for i in range(68, 0, -1):
#         os.makedirs(os.path.join(destination_root, str(i), "men", "Вертикальный"), exist_ok=True)
#         os.makedirs(os.path.join(destination_root, str(i), "men", "Горизонтальный"), exist_ok=True)
    
#     # Проходим по всем файлам в исходной папке
#     for file_name in os.listdir(source_folder):
#         if file_name.endswith(".zip"):
#             file_path = os.path.join(source_folder, file_name)
            
#             # Определяем, в какую папку копировать файл
#             try:
#                 number, orientation = file_name.split(" ")
#                 number = int(number)  # Число перед '_'
                
#                 if orientation.startswith("вер"):
#                     destination = os.path.join(destination_root, str(number), "men", "Вертикальный")
#                 elif orientation.startswith("гор"):
#                     destination = os.path.join(destination_root, str(number), "men", "Горизонтальный")
#                 else:
#                     print(f"Пропущен файл {file_name}: неизвестный тип ориентации.")
#                     continue
                
#                 # Копируем файл в нужную папку
#                 shutil.copy(file_path, destination)
#                 print(f"Файл {file_name} скопирован в {destination}")
#             except ValueError as e:
#                 print(f"Ошибка обработки файла {file_name}: {e}")

# # Укажите пути к папке с zip-файлами и корневой папке назначения
# source_folder = "/root/project/balancer-v2.0/face_to_face_server0/media"  # Путь к папке с zip-файлами
# destination_root = "/root/project/balancer-v2.0/face_to_face_server0/media"  # Путь к корневой папке назначения

# distribute_zip_files(source_folder, destination_root)





import os
import zipfile

def extract_all_zips(root_folder):
    # Проходим по всем папкам, начиная с корневой
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Проверяем, является ли файл .zip архивом
            if filename.endswith('.zip'):
                zip_path = os.path.join(dirpath, filename)
                extract_to = dirpath  # Распаковываем в текущую папку
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_to)
                        print(f"Распакован: {zip_path} в {extract_to}")
                except zipfile.BadZipFile:
                    print(f"Ошибка: файл {zip_path} повреждён или не является zip-архивом.")

# Укажите путь к корневой папке, где находятся 88 папок
root_folder = "/root/project/balancer-v2.0/face_to_face_server0/media"  # Замените на ваш путь

extract_all_zips(root_folder)
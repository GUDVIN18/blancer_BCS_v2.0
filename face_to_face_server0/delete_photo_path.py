import os
import shutil

def clear_directories(base_path, start, end, papka):
    """
    Удаляет содержимое директорий в заданном диапазоне.

    :param base_path: Общий путь до директорий
    :param start: Начальный индекс
    :param end: Конечный индекс
    """
    for i in range(start, end + 1):
        # Формируем путь к директории
        dir_path = os.path.join(base_path, f"{i}_neiro1", papka)
        
        # Проверяем, существует ли директория
        if os.path.exists(dir_path):
            try:
                # Удаляем все файлы и папки внутри
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)  # Удаляем файл или символическую ссылку
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Удаляем папку
                print(f"Очищено содержимое директории: {dir_path}")
            except Exception as e:
                print(f"Ошибка при очистке {dir_path}: {e}")
        else:
            print(f"Директория не найдена: {dir_path}")

base_path = "/root/project/balancer-v2.0/face_to_face_server0/media"
start_index = 1
end_index = 88

# Запуск
papka = 'men'
# papka = 'women'
clear_directories(base_path, start_index, end_index, papka)
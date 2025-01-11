from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.bot_app.views import *
from apps.webui.views import index, upload_photo, task_complete_alert
# from apps.worker_app.views import get_task_status


urlpatterns = [
    path('admin/', admin.site.urls),

    path('get_task_status', get_task_status, name="get_task_status"),
    path('finish_task_status', finish_task_status, name="finish_task_status"),
    path('get_task_result', get_task_result, name="get_task_result"),
    path('create_task', create_task, name="create_task"),
    path('user_waiting', user_waiting, name="user_waiting"),
    path('task_complete_alert/<int:task_id>/', task_complete_alert, name='task_complete_alert'),
    path('get_logs', get_logs, name='get_logs'),


    # обработка от Бота Александра multidata
    # path('create_task_multidata', create_task_multidata, name='create_task_multidata'),
    path('task_status/<int:task_id>/', task_status, name='task_status'),
    path('get_file/<int:task_id>/', get_file, name='get_file'),
    path('deletepath/<path:path>', deletepath, name="deletepath"),
    path('start_generator', start_generator, name="start_generator"),
    path('export-prompt-settings-xlsx', export_prompt_model_settings_xlsx, name='export_prompt_settings_xlsx'),
    path('start_leonardo_generations', start_leonardo_generations, name='start_leonardo_generations'),
    # WebUi для Алексея
    path('upload/', upload_photo, name='upload_photo'),
    
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

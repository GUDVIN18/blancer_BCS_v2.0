import asyncio
from PIL import Image
from asgiref.sync import sync_to_async
from apps.bot_app.models import TelegramBotConfig
from apps.bot_app.models import GenerationProcess, LoggingProccess
from apps.worker_app.models import Server
from apps.stickers.models import Generate_Stickers
from apps.worker_app.views import data_server, data_server_targetphoto
from apps.stickers.models import Stiker_target_photo, StikerPackConfig
import uuid
import time
from datetime import datetime
from apps.stickers.utils import get_stikers_list, send_stikers_pack
from django.utils.timezone import now


from datetime import timedelta




while True:
        servers = Server.objects.filter(status=True)

        for server in servers:
            server_generation = GenerationProcess.objects.filter(server_int=server.id, process_status__in=['ACCEPTED', ])
            
            if server_generation.count() < server.server_max_process:
                tasks = GenerationProcess.objects.filter(process_status='WAITING', server_int=None)
                print('Не принятых процессов', len(tasks))
                # print(f'server_generation {server_generation}\nserver_generation.count() {server_generation.count()}\nserver.server_max_process {server.server_max_process}')
                
                for task in tasks:
                    if task.target_photo != None:
                        # Assign task to this server
                        if server_generation.count() < server.server_max_process:
                            task.server_int = server.id
                            task.save()
                            print('балансировщик Принял')
                            
                            status = data_server_targetphoto(
                                server_name=server.server_name,
                                server_address=server.server_adress,
                                server_port=server.server_port,
                                server_auth_token=server.server_auth_token,
                                server_max_process=server.server_max_process,
                                
                                process_backend_id=uuid.uuid4(),
                                task_id=task.id,
                                file_path=task.photo.image.path,
                                target_path = task.target_photo.image.path,
                            )

                            print('status', status)
                    
                    else:
                        # Assign task to this server
                        if server_generation.count() < server.server_max_process and task.photo.image.path is not None:
                            task.server_int = server.id
                            task.save()
                            print('балансировщик Принял')
                            
                            status = data_server(
                                server_name=server.server_name,
                                server_address=server.server_adress,
                                server_port=server.server_port,
                                server_auth_token=server.server_auth_token,
                                server_max_process=server.server_max_process,
                                
                                process_backend_id=uuid.uuid4(),
                                task_id=task.id,
                                file_path=task.photo.image.path,
                                prompt=task.prompt,
                                negative_prompt=task.negative_prompt,
                                format_photo=task.format_photo,
                            )

                            print('status', status)






            tasks_accepted_time = GenerationProcess.objects.filter(process_status='ACCEPTED', process_start_time=None)
            for task_accepted in tasks_accepted_time:
                task_accepted.process_start_time = now()
                try:
                    loger = LoggingProccess.objects.get(generation_number=task_accepted)
                    loger.process_start_time = now()
                    loger.save()
                except:
                    print('Процесс не найден')
                task_accepted.save()


            tasks_accepted_log = GenerationProcess.objects.filter(process_status='COMPLETED', process_end_time=None)
            for task_accepted in tasks_accepted_log:
                if task_accepted.process_start_time is not None:
                    task_accepted.process_end_time = now()
                    task_accepted.process_take_time = now() - task_accepted.process_start_time
                    task_accepted.save()
                    try:
                        loger = LoggingProccess.objects.get(generation_number=task_accepted)
                        loger.generation_time = task_accepted.process_take_time
                        loger.save()
                    except:
                        print('Процесс не найден')
                        
            time.sleep(0.5)
            tasks_accepted_error = GenerationProcess.objects.filter(process_status='WAITING', server_int=server.id)
            for task_accepted in tasks_accepted_error:
                        
                # if task_accepted.process_start_time is not None:
                #     if now() - task_accepted.process_start_time >= timedelta(seconds=3):
                        task_accepted.server_int = None
                        task_accepted.process_status = 'WAITING'
                        task_accepted.save()


            time.sleep(0.5)
            tasks_accepted_error = GenerationProcess.objects.filter(process_status='ACCEPTED', server_int=server.id)
            for task_accepted in tasks_accepted_error:
                        
                if task_accepted.process_start_time is not None:
                    if now() - task_accepted.process_start_time >= timedelta(seconds=80):
                        task_accepted.server_int = None
                        task_accepted.process_status = 'WAITING'
                        task_accepted.save()
        time.sleep(0.01)
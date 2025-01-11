from django.db import models

class TelegramBotConfig(models.Model):
    bot_token = models.CharField(max_length=100)

    is_activ = models.BooleanField(null=False, blank=False, default=False, verbose_name="Is active")

    def __str__(self):
        return f'{self.bot_token}'

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"


class BotUser(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name="ID Telegram")
    first_name = models.CharField(max_length=250, verbose_name="Имя пользователя", blank=True, null=True)
    last_name = models.CharField(max_length=250, verbose_name="Фамилия пользователя", blank=True, null=True)
    username = models.CharField(max_length=250, verbose_name="Username пользователя", blank=True, null=True)
    language = models.CharField(max_length=250, verbose_name="Язык пользователя", blank=True, null=True)
    premium = models.BooleanField(verbose_name="Имеет ли пользователь премиум-аккаунт", default=False, blank=True, null=True)
    generation = models.BooleanField(default=False, verbose_name="Выполняется ли генерация?")

    def __str__(self):
        return f"{self.tg_id}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"





class Images(models.Model):
    description = models.CharField(max_length=255, default=None, blank=True, null=True)
    image = models.ImageField(upload_to='img_storage/', verbose_name='Хранилище фоток', null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
            verbose_name = "Исходник"
            verbose_name_plural = "Исходники"








class GenerationProcess(models.Model):
    PROCESS_STATUS_CHOICES = [
        ('ACCEPTED', 'Процесс принят сервером на генерацию'),
        ('COMPLETED', 'Генерация успешно завершена'),
        ('WAITING', 'Генерация ожидает принятия сервером'),
        ('ERROR_GENERATION', 'Ошибка генерации'),
    ]

    process_status = models.CharField(max_length=110, choices=PROCESS_STATUS_CHOICES)
    process_backend_id = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    photo = models.ForeignKey(to=Images, verbose_name='Загруженное изображение', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='photo')
    target_photo = models.ForeignKey(to=Images, verbose_name='На кого будет наложено', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='target_photo')
    output_photo = models.ForeignKey(to=Images, verbose_name='Полученное фото после генерации', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='output_photo')
    server_int = models.IntegerField(default=None, null=True, blank=True)

    process_start_time = models.DateTimeField(null=True, blank=True, help_text="Время старта процесса", verbose_name='Старт')
    process_end_time = models.DateTimeField(null=True, blank=True, help_text="Время окончания процесса (если процесс завершен)", verbose_name='Завершение')
    process_take_time = models.DurationField(null=True, blank=True, help_text="Сколько всего времени заняло исполнение процесса (если процесс завершен)", verbose_name='Время выполнения')

    prompt = models.TextField(null=True, blank=True, help_text='user prompt')
    negative_prompt =  models.TextField(verbose_name="Негативный Промпт", null=True, blank=True)
    
    textovka_new = models.CharField(max_length=500, verbose_name='Готовая текстовка', null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telegram id')
    format_photo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Формат фотки', default='Вертикальный')
    path_on_tahe_photo =  models.TextField(null=True, blank=True, help_text='path on tahe new photo')
    is_alert_sent = models.BooleanField(null=True, blank=True)

    time_completed = models.DateTimeField(default=None, null=True, blank=True)
    task_end_handler = models.CharField(max_length=255, null=True, blank=True, verbose_name='Хендлер завершения таска')
    
    class Meta:
        verbose_name = "Созданный процесс"
        verbose_name_plural = "Созданные процессы"

    def __str__(self):
        return f"Process {self.process_backend_id} - {self.get_process_status_display()}"



class PromptModelSettings(models.Model):
    BUDGET_CHOICES = [
        ('25', '25 тыс. рублей'),
        ('50', '50 тыс. рублей'),
        ('100', '100 тыс. рублей'),
        ('250', '250 тыс. рублей'),
        ('500', '500 тыс. рублей'),
        ('1', '1 млн рублей'),
    ]
    INTEREST_CHOICES = [
        ('Путешествия', 'Путешествия'),
        ('Недвижимость', 'Недвижимость'),
        ('Развлечения', 'Развлечения'),
        ('Автомобили', 'Автомобили'),
        ('Саморазвитие', 'Саморазвитие'),
        ('Эмоции / Вдохновение', 'Эмоции / Вдохновение'),
    ]
    number = models.IntegerField(verbose_name="Номер промта", null=True, blank=True)
    rolevaya = models.CharField(max_length=300, verbose_name="Ролевая", null=True, blank=True)
    purpose = models.CharField(max_length=600, verbose_name="Назначение", null=True, blank=True)

    promt_russia = models.TextField(verbose_name="Промпт на рус", null=True, blank=True)
    promt_english = models.TextField(verbose_name="Промпт на англ", null=True, blank=True)
    
    men_promt = models.TextField(verbose_name="Мужской Промпт", null=True, blank=True)
    women_promt = models.TextField(verbose_name="Женский Промпт", null=True, blank=True)

    negative_prompt =  models.TextField(verbose_name="Негативный Промпт", null=True, blank=True)

    interest_1 = models.CharField(max_length=500, choices=INTEREST_CHOICES, verbose_name="Интерес 1", null=True, blank=True)
    interest_2 = models.CharField(max_length=500, choices=INTEREST_CHOICES, verbose_name="Интерес 2", null=True, blank=True)
    budget_1 = models.CharField(max_length=500, choices=BUDGET_CHOICES, verbose_name="Бюджет 1", null=True, blank=True)
    budget_2 = models.CharField(max_length=500, choices=BUDGET_CHOICES, verbose_name="Бюджет 2", null=True, blank=True)
    budget_3 = models.CharField(max_length=500, choices=BUDGET_CHOICES, verbose_name="Бюджет 3", null=True, blank=True)
    text = models.TextField(verbose_name="После", null=True, blank=True)

    def __str__(self):
        return f"{self.purpose or 'Без назначения'} ({self.number})"






class LoggingProccess(models.Model):
    user_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telegram id')
    generation_number = models.ForeignKey(to=GenerationProcess, verbose_name='Процесс', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT, related_name='generation_number')

    process_start_time = models.DateTimeField(null=True, blank=True, help_text="Время старта процесса", verbose_name='Старт')
    generation_time = models.DurationField(null=True, blank=True, help_text="Сколько всего времени заняло исполнение процесса (если процесс завершен)", verbose_name='Время выполнения', )

    result_formula = models.TextField(verbose_name='Результат формулы', null=True, blank=True)
    user_price = models.CharField(max_length=999, verbose_name='Сумма', null=True, blank=True)
    
    user_category = models.CharField(max_length=255, verbose_name='Интерес', null=True, blank=True)
    gender = models.CharField(max_length=255, verbose_name='Гендер', null=True, blank=True)
    time_invest = models.CharField(max_length=255, verbose_name='На какой срок', null=True, blank=True)
    investor_risk = models.CharField(max_length=255, verbose_name='Риски', null=True, blank=True)
    textovka_new = models.CharField(max_length=500, verbose_name='Готовая текстовка', null=True, blank=True)
    


    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"

    def __str__(self):
        return f"Process {self.id} - {self.user_id}"

# Register your models here.
from django.contrib import admin
from .models import *

# admin.site.register(TelegramBotConfig)
# admin.site.register(BotUser)
# admin.site.register(GenerationProcess)
# admin.site.register(Images)


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    fields = [
        "description",
        'image',
    ]
    list_display = (
        "id",
        "description",
        'image',
    )
    list_filter = (
        "description",
    )




@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    fields = [
        "bot_token",
        'is_activ',
    ]
    list_display = (
        "id",
        "bot_token",
        'is_activ',
    )
    list_filter = (
        "bot_token",
        'is_activ',
    )
    search_fields = (
        "bot_token",
    )


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    fields = [
        "tg_id",
        "first_name",
        "last_name",
        "username",
        "language",
        "premium",
        "generation"

    ]
    list_display = (
        "tg_id",
        "first_name",
        "username",
        "generation"
    )
    list_filter = (
        "tg_id",
        "username",
        "generation"

    )
    search_fields = (
        "tg_id",
        "username",
        "id"
    )



@admin.register(GenerationProcess)
class GenerationProcessAdmin(admin.ModelAdmin):
    fields = [
        "process_status",
        "process_backend_id",
        'user_id',
        'process_start_time',
        'process_end_time',
        'process_take_time',
        "prompt",
        "negative_prompt",
        "textovka_new",
        "format_photo",
        "photo",
        "target_photo",
        "output_photo",
        'server_int',
        'task_end_handler',
        'path_on_tahe_photo',
        'is_alert_sent',

    ]
    list_display = (
        'id',
        "process_status",
        "format_photo",
        'server_int'
    )
    list_filter = (
        "process_status",

    )
    search_fields = (
        "user",
        "process_backend_id",
        "id"
    )






@admin.register(PromptModelSettings)
class PromptModelSettingsAdmin(admin.ModelAdmin):
    fields = [
        "number",
        "rolevaya",
        "purpose",
        "men_promt",
        "women_promt",
        "negative_prompt",
        "interest_1",
        "interest_2",
        "budget_1",
        "budget_2",
        "budget_3",
        "text"
    ]
    list_display = (
        "number",
        "purpose",
        "interest_1",
        "interest_2",
        "budget_1",
        "budget_2",
        "budget_3",
    )
    list_filter = (
        "rolevaya",
        "interest_1",
        "interest_2",
        "budget_1",
        "budget_2",
        "budget_3",
    )
    search_fields = (
        "purpose",
        "promt_russia",
        "promt_english",
    )




@admin.register(LoggingProccess)
class LoggingProccessAdmin(admin.ModelAdmin):
    fields = [
        "user_id",
        "generation_number",
        'process_start_time',
        "generation_time",
        "result_formula",
        "user_price",
        "user_category",
        "gender",
        "time_invest",
        "investor_risk",
        "textovka_new",
    ]
    list_display = (
        "id",
        "user_id",
        'process_start_time',
        "generation_time",
        "result_formula",  # Используем кастомный метод для отображения
        "user_price",
        "user_category",
        "gender",
        "time_invest",
        "investor_risk",
        "generation_number",
    )
    list_filter = (
        "process_start_time",
        "gender",
        "user_category",
        "investor_risk",
    )
    search_fields = (
        "user_id",
        "user_category",
        "gender",
        "time_invest",
        "investor_risk",
    )


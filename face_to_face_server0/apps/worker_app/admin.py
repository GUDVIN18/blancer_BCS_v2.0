from django.contrib import admin
from .models import Server, InswapperConfig

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    fields = [
        # "id",
        "server_name",
        'status',
        "server_adress",
        "server_port",
        "server_auth_token",
        "server_max_process",
        "last_rec_date",
    ]
    list_display = (
        "id",
        'status',
        "server_name",
        "server_adress",
        "server_max_process",
        # "",
    )
    # readonly_fields = (
    #     "",
    #     "",
    # )
    list_filter = (
        "status",
        "server_name",
        "server_adress",
        "server_port",
        "server_max_process",   
    )
    search_fields = (
        "status",
        "server_name",
        "server_adress",
        "server_port",
        "server_max_process",
    )


@admin.register(InswapperConfig)
class InswapperConfigAdmin(admin.ModelAdmin):
    fields = [
        "upscale",
        "codeformer_fidelity",
    ]
    list_display = (
        "id",
        "upscale",
        "codeformer_fidelity",
    )
    # readonly_fields = (
    #     "",
    #     "",
    # )
    list_filter = (
        "upscale",
        "codeformer_fidelity",
    )
    search_fields = (
        "upscale",
        "codeformer_fidelity",
    )
# Generated by Django 5.1.1 on 2024-12-12 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0024_loggingproccess_textovka_new_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loggingproccess',
            name='textovka_new',
        ),
        migrations.AddField(
            model_name='generationprocess',
            name='textovka_new',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Готовая текстовка'),
        ),
    ]

# Generated by Django 5.1 on 2024-12-09 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0006_promptmodelsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='and_or_and_you',
            field=models.CharField(choices=[('AND', 'И'), ('AND_YOU', 'И вы')], max_length=300, verbose_name='И / Или'),
        ),
    ]

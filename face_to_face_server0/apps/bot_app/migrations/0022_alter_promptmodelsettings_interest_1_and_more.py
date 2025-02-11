# Generated by Django 5.1.1 on 2024-12-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0021_alter_promptmodelsettings_budget_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='interest_1',
            field=models.CharField(blank=True, choices=[('Путешествия', 'Путешествия'), ('Недвижимость', 'Недвижимость'), ('Развлечения', 'Развлечения'), ('Автомобили', 'Автомобили'), ('Саморазвитие', 'Саморазвитие'), ('Эмоции / Вдохновение', 'Эмоции / Вдохновение')], max_length=500, null=True, verbose_name='Интерес 1'),
        ),
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='interest_2',
            field=models.CharField(blank=True, choices=[('Путешествия', 'Путешествия'), ('Недвижимость', 'Недвижимость'), ('Развлечения', 'Развлечения'), ('Автомобили', 'Автомобили'), ('Саморазвитие', 'Саморазвитие'), ('Эмоции / Вдохновение', 'Эмоции / Вдохновение')], max_length=500, null=True, verbose_name='Интерес 2'),
        ),
    ]

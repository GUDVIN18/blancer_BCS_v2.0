# Generated by Django 5.1.1 on 2024-12-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0020_alter_promptmodelsettings_budget_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='budget_1',
            field=models.CharField(blank=True, choices=[('25', '25 тыс. рублей'), ('500', '50 тыс. рублей'), ('100', '100 тыс. рублей'), ('250', '250 тыс. рублей'), ('500', '500 тыс. рублей'), ('1', '1 млн рублей')], max_length=500, null=True, verbose_name='Бюджет 1'),
        ),
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='budget_2',
            field=models.CharField(blank=True, choices=[('25', '25 тыс. рублей'), ('500', '50 тыс. рублей'), ('100', '100 тыс. рублей'), ('250', '250 тыс. рублей'), ('500', '500 тыс. рублей'), ('1', '1 млн рублей')], max_length=500, null=True, verbose_name='Бюджет 2'),
        ),
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='budget_3',
            field=models.CharField(blank=True, choices=[('25', '25 тыс. рублей'), ('500', '50 тыс. рублей'), ('100', '100 тыс. рублей'), ('250', '250 тыс. рублей'), ('500', '500 тыс. рублей'), ('1', '1 млн рублей')], max_length=500, null=True, verbose_name='Бюджет 3'),
        ),
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='interest_1',
            field=models.CharField(blank=True, choices=[('Путешествия', 'Путешествия'), ('Недвижимость', 'Недвижимость'), ('Развлечения', 'Развлечения'), ('Автомобили', 'Автомобили'), ('Саморазвитие', 'Саморазвитие'), ('Эмоции/Вдохновение', 'Эмоции/Вдохновение')], max_length=500, null=True, verbose_name='Интерес 1'),
        ),
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='interest_2',
            field=models.CharField(blank=True, choices=[('Путешествия', 'Путешествия'), ('Недвижимость', 'Недвижимость'), ('Развлечения', 'Развлечения'), ('Автомобили', 'Автомобили'), ('Саморазвитие', 'Саморазвитие'), ('Эмоции/Вдохновение', 'Эмоции/Вдохновение')], max_length=500, null=True, verbose_name='Интерес 2'),
        ),
    ]

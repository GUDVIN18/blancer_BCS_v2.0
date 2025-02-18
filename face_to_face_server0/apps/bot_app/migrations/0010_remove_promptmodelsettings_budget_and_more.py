# Generated by Django 5.1.1 on 2024-12-11 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0009_alter_promptmodelsettings_budget_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promptmodelsettings',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='promptmodelsettings',
            name='interest',
        ),
        migrations.AddField(
            model_name='promptmodelsettings',
            name='budget_1',
            field=models.CharField(blank=True, choices=[('25', '25 тыс. рублей'), ('500', '50 тыс. рублей'), ('100', '100 тыс. рублей'), ('250', '250 тыс. рублей'), ('500', '500 тыс. рублей'), ('1', '1 млн рублей')], max_length=500, null=True, verbose_name='Бюджет'),
        ),
        migrations.AddField(
            model_name='promptmodelsettings',
            name='budget_2',
            field=models.CharField(blank=True, choices=[('25', '25 тыс. рублей'), ('500', '50 тыс. рублей'), ('100', '100 тыс. рублей'), ('250', '250 тыс. рублей'), ('500', '500 тыс. рублей'), ('1', '1 млн рублей')], max_length=500, null=True, verbose_name='Бюджет'),
        ),
        migrations.AddField(
            model_name='promptmodelsettings',
            name='budget_3',
            field=models.CharField(blank=True, choices=[('25', '25 тыс. рублей'), ('500', '50 тыс. рублей'), ('100', '100 тыс. рублей'), ('250', '250 тыс. рублей'), ('500', '500 тыс. рублей'), ('1', '1 млн рублей')], max_length=500, null=True, verbose_name='Бюджет'),
        ),
        migrations.AddField(
            model_name='promptmodelsettings',
            name='interest_1',
            field=models.CharField(blank=True, choices=[('Путешествия', 'Путешествия'), ('Недвижимость', 'Недвижимость'), ('Развлечения', 'Развлечения'), ('Автомобили', 'Автомобили'), ('Саморазвитие', 'Саморазвитие'), ('Эмоции/Вдохновение', 'Эмоции/Вдохновение')], max_length=500, null=True, verbose_name='Интерес'),
        ),
        migrations.AddField(
            model_name='promptmodelsettings',
            name='interest_2',
            field=models.CharField(blank=True, choices=[('Путешествия', 'Путешествия'), ('Недвижимость', 'Недвижимость'), ('Развлечения', 'Развлечения'), ('Автомобили', 'Автомобили'), ('Саморазвитие', 'Саморазвитие'), ('Эмоции/Вдохновение', 'Эмоции/Вдохновение')], max_length=500, null=True, verbose_name='Интерес'),
        ),
        migrations.AddField(
            model_name='promptmodelsettings',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='После и/и вы'),
        ),
        migrations.AlterField(
            model_name='promptmodelsettings',
            name='and_or_and_you',
            field=models.CharField(blank=True, choices=[('AND', 'И'), ('AND_YOU', 'И Вы')], max_length=300, null=True, verbose_name='И / И Вы'),
        ),
    ]

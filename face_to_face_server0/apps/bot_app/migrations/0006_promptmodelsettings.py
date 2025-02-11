# Generated by Django 5.1 on 2024-12-09 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0005_generationprocess_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromptModelSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('and_or_and_you', models.CharField(choices=[('AND', 'И'), ('OR', 'Или')], max_length=3, verbose_name='И / Или')),
                ('purpose', models.CharField(blank=True, max_length=600, null=True, verbose_name='Назначение')),
                ('promt_english', models.TextField(blank=True, null=True, verbose_name='Промпт на англ')),
                ('interest', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], max_length=1, verbose_name='Интерес')),
                ('budget', models.CharField(choices=[('Z', 'Z'), ('X', 'X'), ('C', 'C'), ('V', 'V'), ('F', 'F'), ('L', 'L')], max_length=1, verbose_name='Бюджет')),
            ],
        ),
    ]

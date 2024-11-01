# Generated by Django 5.1.1 on 2024-10-22 18:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('street', models.CharField(max_length=100, verbose_name='Улица')),
                ('house', models.CharField(max_length=10, verbose_name='Дом')),
                ('building', models.CharField(blank=True, max_length=10, verbose_name='Строение')),
                ('flat', models.IntegerField(blank=True, verbose_name='Квартира')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]

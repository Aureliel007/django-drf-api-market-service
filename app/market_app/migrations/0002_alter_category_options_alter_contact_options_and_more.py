# Generated by Django 5.1.1 on 2025-01-08 20:21

import easy_thumbnails.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Магазин'),
        ),
    ]

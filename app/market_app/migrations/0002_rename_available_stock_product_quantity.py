# Generated by Django 5.1.1 on 2024-11-02 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='available_stock',
            new_name='quantity',
        ),
    ]

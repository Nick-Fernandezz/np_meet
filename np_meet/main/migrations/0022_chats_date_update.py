# Generated by Django 4.2.2 on 2023-07-11 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_chats_type_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='date_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]

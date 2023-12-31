# Generated by Django 4.2.2 on 2023-07-10 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_tasks_options_chats'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='type',
            field=models.CharField(choices=[('private', 'Приватный'), ('public', 'Публичный'), ('channel', 'Канал')], default='private', max_length=100),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=2000, verbose_name='Сообщение')),
                ('send_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('edit_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата изменения')),
                ('is_pin', models.BooleanField(default=False, verbose_name='Закреплено')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.chats', verbose_name='Чат')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
    ]

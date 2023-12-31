# Generated by Django 4.2.2 on 2023-07-02 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0019_tasks_active_alter_user_email'),
        ('logs', '0004_alter_logauthuser_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('do', models.CharField(default='', max_length=100, verbose_name='Действие')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.corporations', verbose_name='компания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'лог задачи',
                'verbose_name_plural': 'Логи задачь',
            },
        ),
    ]

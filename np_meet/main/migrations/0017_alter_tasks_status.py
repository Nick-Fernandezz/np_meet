# Generated by Django 4.2.2 on 2023-07-01 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_tasks_options_tasks_is_new_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(blank=True, choices=[('done', 'Выполнено'), ('in_process', 'В процессе'), ('in_start', 'Не начат')], max_length=50, null=True),
        ),
    ]

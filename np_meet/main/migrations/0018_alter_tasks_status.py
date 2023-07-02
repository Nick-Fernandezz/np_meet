# Generated by Django 4.2.2 on 2023-07-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[('done', 'Выполнено'), ('in_process', 'В процессе'), ('in_start', 'Не начат')], default='in_start', max_length=50),
        ),
    ]
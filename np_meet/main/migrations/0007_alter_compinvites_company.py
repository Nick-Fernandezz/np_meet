# Generated by Django 4.2.2 on 2023-06-20 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_compinvites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compinvites',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.corporations', verbose_name='компания'),
        ),
    ]

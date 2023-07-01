from django.db import models
from main.models import *
# Create your models here.


class LogsInvites(models.Model):

    company = models.ForeignKey(Corporations, on_delete=models.DO_NOTHING, verbose_name='компания')
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    code = models.CharField(max_length=100, verbose_name='Код приглашения')
    do = models.TextField(verbose_name='Действие', max_length=300, default='')
    created_date = models.DateTimeField(verbose_name='Время', auto_now_add=True)

    class Meta:
        verbose_name =  'лог приглашения'
        verbose_name_plural = 'Логи приглашений'

    def __str__(self) -> str:
        return self.code


class LogAuthUser(models.Model):
    company = models.ForeignKey(Corporations, on_delete=models.DO_NOTHING, verbose_name='компания', null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    date_login = models.DateTimeField(auto_now_add=True, verbose_name='Дата входа')
    do = models.CharField(max_length=100, verbose_name='Действие', default='')

    class Meta:
        verbose_name =  'лог авторизации'
        verbose_name_plural = 'Логи авторизаций'
        
    def __str__(self) -> str:
        return str(self.id)

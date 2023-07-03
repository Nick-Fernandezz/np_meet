from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserPermisions(models.Model):
    permission = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.permission)

class Corporations(models.Model):

    name = models.CharField('Название компании', max_length=100)
    logo = models.ImageField('Логотип компании', upload_to='main/corporation/logos')
    directors = models.ForeignKey('main.User', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return str(self.name)

class CorpPositions(models.Model):
    corporation = models.ForeignKey(Corporations, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    permisions_user = models.ManyToManyField(UserPermisions)

    def __str__(self) -> str:
        return str(self.corporation)

class User(AbstractUser):

    avatar = models.ImageField(upload_to='main/users/avatars', default='main/users/avatars/default.webp')
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    position = models.ManyToManyField(CorpPositions, blank=True)
    corporation = models.ForeignKey(Corporations, on_delete=models.CASCADE, null=True, blank=True)
    reg_ip = models.GenericIPAddressField(verbose_name='IP при регистрации', blank=True, null=True)
    last_ip = models.GenericIPAddressField(verbose_name='IP последнего входа', blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.username)


class CompInvites(models.Model):

    company = models.ForeignKey(Corporations, on_delete=models.CASCADE, verbose_name='компания')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    code = models.CharField(max_length=100, verbose_name='Код приглашения')
    activations = models.IntegerField(verbose_name='Количество активаций', default=0)
    max_activations = models.IntegerField(verbose_name='Максимальное количество активаций')
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    created_date = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, editable=True)
    last_invite = models.DateTimeField(verbose_name='Время последнего присоеденения', auto_now=True)

    class Meta:
        verbose_name =  'приглашение'
        verbose_name_plural = 'Приглашения'
    
    def __str__(self) -> str:
        return str(self.code)
    
class Tasks(models.Model):

    status_option = (
        ('done', 'Выполнено'),
        ('in_process', 'В процессе'),
        ('in_start', 'Не начат'),
    )

    company = models.ForeignKey(Corporations, on_delete=models.CASCADE, verbose_name='Компания')
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Поручитель', related_name='user_creator')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Работник', related_name='user_worker')
    task = models.TextField(verbose_name='Задача')
    status = models.CharField(choices=status_option, max_length=50, default=status_option[2][0])
    is_new = models.BooleanField(verbose_name='Новая', default=True)
    active = models.BooleanField(verbose_name='Активная', default=True)
    created_date = models.DateTimeField(verbose_name='Дата поручения', auto_now_add=True)
    deadline = models.DateTimeField(verbose_name='Дедлайн')

    class Meta:
        verbose_name = 'задачу  '
        verbose_name_plural = 'Задачи'
    
    def __str__(self) -> str:
        return self.task[:20]
    
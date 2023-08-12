from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# from django.contrib.auth import AnonymousUser
from django.db import IntegrityError
from .models import *
from logs.models import *
from .forms import *
from .scripts.random_invite_code import random_code
from django.contrib.auth.decorators import login_required
from .views_scripts import auth as auth_scripts
from .views_scripts import log as log_scripts
# from django.http.response import HttpResponseNotFound


# Create your views here.
def index_page(request):
    if not request.user.is_authenticated:
        return render(request, 'main/index.html')
    else:
        return redirect('control_palen_page')


def singup_user_page(request):

    errors = {
        'incorrectpassword': 'Пароли не совпадают',
        'incorrectusername': 'Пользователь с таким именем пользователя или почтой уже зарегистрирован, попробуйте авторизоваться'
    }

    
    if request.method == 'POST':
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    email=request.POST['email'],
                    password=request.POST['password1'],
                    
                )
                user.reg_ip, user.last_ip = auth_scripts.get_ip(request), auth_scripts.get_ip(request)
                log_scripts.create_log_auth(request, 'Зарегистрировался')
                user.save()
                login(request, user)
                return redirect('home_page')
            else:
                return render(request, 'main/singup_user_page.html', context={
                    'form': SingUPForm(),
                    'error': errors['incorrectpassword'],
                    })      
        except IntegrityError:
            return render(request, 'main/singup_user_page.html', context={
                        'form': SingUPForm(),
                        'error': errors['incorrectusername'],
                        })   

    else:
        return render(request, 'main/singup_user_page.html', context={'form': SingUPForm()})
    
@login_required
def logoutuser(request):
    if request.method == 'POST':
        log_scripts.create_log_auth(request, 'Вышел из аккаунта')
        logout(request)
        return redirect('home_page')


def login_user_page(request):
    if request.method == 'GET':
        return render(request, 'main/login_user_page.html', context={'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main/login_user_page.html', context={'form': AuthenticationForm(), 
                                                                         'error': 'Пользователь с таким именем не найден'})
        else:
            log_scripts.create_log_auth(request, 'Авторизировался', user=user)
            login(request, user)
            return redirect('control_palen_page')

@login_required
def control_palen_page(request):
    log_scripts.create_log_auth(request, 'Зашел в контрольную панель')
    try:
        corp = Corporations.objects.get(name=request.user.corporation.name)
        return render(request, 'main/contol_panel_page.html', context={
        'corp': corp})
    except ObjectDoesNotExist:
        return render(request, 'main/contol_panel_page.html')
    except MultipleObjectsReturned:
        # print("Найдено более одного объекта")
        return render(request, 'main/contol_panel_page.html', context={
            'corp': corp})
    except:
        return render(request, 'main/contol_panel_page.html')

@login_required
def create_comp_page(request):
    if request.method == 'GET': 
        form = CreateCompanyForm()
        return render(request, 'main/create_comp_page.html', context={'form': form})
    else:
        userform = CreateCompanyForm(request.POST, request.FILES)
        if userform.is_valid():

            newcorp = userform.save(commit=False)
            newcorp.directors = request.user
            newcorp.save()

            return redirect('control_palen_page')
        else:
            form = CreateCompanyForm()
            return render(request, 'main/create_comp_page.html', context={'form': form, 'error': 'Введены некоректные данные'})


@login_required
def company_workers_page(request):

    workers = User.objects.filter(corporation=request.user.corporation)
    invites = CompInvites.objects.filter(company=request.user.corporation, is_active=True)
    return render(request, 'main/corp_workers_page.html', context={
        'workers': workers,
        'invites': invites,
    })

@login_required
def profile_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    director = False
    if request.user.corporation == user.corporation and Corporations.objects.get(name=request.user.corporation.name, directors=request.user):
        director = True
    return render(request, 'main/user_profile_page.html', context={
        'user': user,
        'is_director': director,
    })

@login_required
def delete_worker_invite(request, invite_id):
    invite = CompInvites.objects.get(id=invite_id)
    log_scripts.create_log_invite(request, 'Удалил приглашение', invite.code)
    invite.delete()
    return redirect('company_workers_page')

@login_required
def create_worker_invite(request):
    if request.method == 'GET':
        return render(request, 'main/create_worker_invite.html', context={
            'form': CreateWorckerInviteForm()
        })
    else:
        
        max_activations = int(request.POST.get('max_activations'))
        if 0 < max_activations <= 250:

            new_invite = CompInvites.objects.create(
                company=request.user.corporation, 
                max_activations=max_activations,
                creator=request.user,
                code=random_code()
                ) 
            log_scripts.create_log_invite(request, 'Создал приглашение', new_invite.code)
            new_invite.save()
            return redirect('company_workers_page')
        else:
            return render(request, 'main/create_worker_invite.html', context={
            'form': CreateWorckerInviteForm(),
            'error': 'Ошибка в параметрах. Максимум 250 активаций'
        })

@login_required
def join_worker_invite(request):
    if request.method == 'GET':
        return render(request, 'main/join_worker_invite_page.html', context={
            'form': JoinWorkerInviteForm()
        })
    else:
        userform = JoinWorkerInviteForm(request.POST)
        if userform.is_valid():
            try:
                invite = CompInvites.objects.get(code=request.POST['code'])
                if invite.activations < invite.max_activations:
                    invite.activations = invite.activations + 1
                    user_comp = User.objects.get(username=request.user.username)
                    user_comp.corporation = invite.company
                    user_comp.save()
                    log_scripts.create_log_invite(request, 'Принял приглашение', invite.code, invite.creator)
                    invite.save()
                    
                    return redirect('control_palen_page')
                else:
                    return render(request, 'main/join_worker_invite_page.html', context={
                            'form': JoinWorkerInviteForm(),
                            'error': 'Активации этого кода закончились. Попросите новый код у руководителя',
                        })
            except ObjectDoesNotExist:
                return render(request, 'main/join_worker_invite_page.html', context={
                            'form': JoinWorkerInviteForm(),
                            'error': 'Код не существует',
                        })


## ДОБАВИТЬ ЛОГИРОВАНИЕ УВОЛЬНЕНИЙ

@login_required
def fire_worker(request, user_id):

    if Corporations.objects.filter(directors=request.user).exists() and request.user.id != user_id:
        try:
            worker = User.objects.get(id=user_id)
            worker.corporation = None
            worker.save()
            return redirect('company_workers_page')
        except ObjectDoesNotExist:
            return redirect('company_workers_page')
    else:
        return profile_page(request, user_id)

@login_required
def company_profile_page(request, comp_id):

    if comp_id == request.user.corporation.id:
        company = get_object_or_404(Corporations, id=comp_id)

        workers = User.objects.filter(corporation=comp_id)

        return render(request, 'main/company_profile_page.html', context={
            'comp': company,
            'workers': workers,
        })
    else:
        redirect('control_palen_page')


@login_required
def edit_worker_profile(request):
    if request.method == 'GET':
        form = EditUserForm(instance=request.user)
        return render(request, 'main/edit_worker_profile_page.html', context={
            'form': form
        })
    else:
        form = EditUserForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('control_palen_page')
        else:
            return render(request, 'main/edit_worker_profile_page.html', context={
            'form': EditUserForm(instance=request.user),
            'error': 'Ошибка в введенных данных'
            })


@login_required
def index_tasks_page(request):
    
    return render(request, 'main/tasks/tasks_page.html', context={
        'complete_tasks': Tasks.objects.filter(
            company=request.user.corporation, 
            worker=request.user, 
            status='done', 
            active=True
        ).order_by('deadline'),
        'in_process_tasks': Tasks.objects.filter(
            company=request.user.corporation, 
            worker=request.user, 
            status='in_process', 
            active=True
        ).order_by('deadline'),
        'in_start_tasks': Tasks.objects.filter(
            company=request.user.corporation, 
            worker=request.user, 
            status='in_start', 
            is_new=False, 
            active=True
        ).order_by('deadline'),
        'is_new': Tasks.objects.filter(
            company=request.user.corporation, 
            worker=request.user, 
            is_new=True, 
            active=True
        ).order_by('deadline')
        
    })


@login_required
def detal_task_page(request, task_id):
    task = get_object_or_404(Tasks, company=request.user.corporation, worker=request.user, id=task_id)
    if request.method == 'GET':
        task.is_new = False
        log_scripts.create_log_tasks(request,
                                     text=f'Просмотрел задачу #7')
        
        task.save()
        return render(request, 'main/tasks/detal_task_page.html', context={
            'task': task,
            'statuses': Tasks.status_option
        })
    else:
        status = request.POST['status']
        log_scripts.create_log_tasks(request,
                                     text=f'Изменил статус задачи #{task.id} c {task.status} на {status}')
        task.status = status
        task.save()
        return render(request, 'main/tasks/detal_task_page.html', context={
            'task': task,
            'statuses': Tasks.status_option
        })

@login_required
def hide_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Tasks, company=request.user.corporation, worker=request.user, id=task_id)
        task.active = False
        log_scripts.create_log_tasks(request,
                                     text=f'Скрыл задачу #{task.id}')
        task.save()
        return redirect('index_tasks_page')


@login_required
def hidden_tasks_page(request):
    return render(request, 'main/tasks/hidden_tasks_page.html', context={
        'tasks': Tasks.objects.filter(
            company=request.user.corporation, 
            worker=request.user, 
            active=False
        ).order_by('deadline')
    })


@login_required
def create_task_page(request):
    if request.method == 'GET':
        return render(request, 'main/tasks/create_task_page.html', context={
            'form': CreateTaskForm(company=request.user.corporation)
        })
    else:
        userform = CreateTaskForm(request.POST)
        if userform.is_valid():
            newtask = userform.save(commit=False)
            newtask.creator = request.user
            newtask.company = request.user.corporation
            log_scripts.create_log_tasks(request,
                                     text=f'Создал задачу для @{newtask.worker.username}')
            newtask.save()
            return redirect('index_tasks_page')


@login_required
def mail_page(request):
    chats = Chats.objects.filter(users__id__icontains=request.user.id).order_by('date_update')
    # messages = Messages.objects.filter(chat=chats.first())
    return render(request, 'main/mail/index_mail_page.html', context={
        'chats': chats,
        # 'messages': messages
    })


@login_required
def chat_mail_page(request, chat_id):
    chats = Chats.objects.filter(users__id__icontains=request.user.id).order_by('date_update')
    messages = Messages.objects.filter(chat__id=chat_id)
    return render(request, 'main/mail/index_mail_page.html', context={
        'chats': chats,
        'messages': messages
    })

@login_required
def send_message(request):
    pass

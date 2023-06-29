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
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip = ''
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                user.reg_ip, user.last_ip = ip, ip
                log_auth = LogAuthUser.objects.create(
                    user=user,
                    do='Зарегистрировался'
                )
                log_auth.save()
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
        log_auth = LogAuthUser.objects.create(
                    company=request.user.corporation,
                    user=request.user,
                    do='Вышел из аккаунта'
                )
        log_auth.save()
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
            log_auth = LogAuthUser.objects.create(
                    company=user.corporation,
                    user=user,
                    do='Авторизировался'
                )
            log_auth.save()
            login(request, user)
            return redirect('control_palen_page')

@login_required
def control_palen_page(request):
    log_auth = LogAuthUser.objects.create(
                    company=request.user.corporation,
                    user=request.user,
                    do='Зашел в контрольную панель'
                )
    log_auth.save()
    try:
        corp = Corporations.objects.get(name=request.user.corporation.name)
        # print(corp)
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
    log = LogsInvites.objects.create(
            company=request.user.corporation,
            creator=request.user,
            code=invite.code,
            do='Удалил приглашение'

        )
    log.save()
    invite.delete()
    # print(invite.code)
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
            log = LogsInvites.objects.create(
                company=request.user.corporation,
                creator=request.user,
                code=new_invite.code,
                do='Создал приглашение'

            )
            log.save()
            # new_invite.max_activations = max_activationsForm
            # new_invite.company = request.user.comporation
            # new_invite.creator = request.user
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
                    log = LogsInvites.objects.create(
                        company=user_comp.corporation,
                        creator=invite.creator,
                        code=invite.code,
                        do='Создал приглашение'

                    )
                    log.save()
                    invite.save()
                    user_comp.save()
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
        print(request.user.id)
        return render(request, 'main/edit_worker_profile_page.html', context={
            'form': form
        })
    else:
        form = EditUserForm(data=request.POST, files=request.FILES, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('control_palen_page')
        else:
            return render(request, 'main/edit_worker_profile_page.html', context={
            'form': EditUserForm(instance=request.user),
            'error': 'Ошибка в введенных данных'
            })



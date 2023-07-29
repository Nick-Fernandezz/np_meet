from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
# Create your views here.

def index_log_page(request):
    return redirect('invites_log_page')

@login_required
def invites_log_page(request):
    s_data = request.GET.get('q')
    page_number = request.GET.get('page')
    if not page_number: page_number = 1
    if s_data:
        
        logs = Paginator(LogsInvites.objects.filter(Q(company=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(creator__username=s_data) | 
            Q(code=s_data) |
            Q(do=s_data))).order_by('-created_date'), 40)
        
            
        return render(request, 'logs/invites_log_page.html', context={
            'logs': logs.get_page(page_number)
        })
    else:
        logs = Paginator(LogsInvites.objects.filter(company=request.user.corporation).order_by('-created_date'), 100)
        return render(request, 'logs/invites_log_page.html', context={
            'logs': logs.get_page(page_number)
        })

@login_required
def auth_log_page(request):
    s_data = request.GET.get('q')
    page_number = request.GET.get('page')
    if not page_number: page_number = 1
    if s_data:
        
        logs = Paginator(LogAuthUser.objects.filter(Q(company=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(user__username=s_data) | 
            Q(do=s_data))).order_by('-date_login'), 40)
        

        return render(request, 'logs/auth_log_page.html', context={
            'logs': logs.get_page(page_number)
        })
    else:
        logs = Paginator(LogAuthUser.objects.filter(company=request.user.corporation).order_by('-date_login'),
                         40)
        if not page_number: page_number = 1
        return render(request, 'logs/auth_log_page.html', context={
            'logs': logs.get_page(page_number)
        })
    
    

def tasks_log_page(request):
    page_number = request.GET.get('page')
    if not page_number: page_number = 1
    s_data = request.GET.get('q')
    if s_data:
        
        logs = Paginator(LogTasks.objects.filter(Q(user__corporation=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(user__username__icontains=s_data) | 
            Q(do__icontains=s_data))).order_by('-date'), 40)
        if s_data.isdigit():
            tasks = Paginator(Tasks.objects.filter(Q(company=request.user.corporation) & (
                Q(company__name=s_data) | 
                Q(worker__username__icontains=s_data) | 
                Q(creator__username__icontains=s_data) | 
                Q(task__icontains=s_data) |
                Q(id=s_data) |  
                Q(status__icontains=s_data))).order_by('-created_date'), 40)
        else:
            tasks = Paginator(Tasks.objects.filter(Q(company=request.user.corporation) & (
                Q(company__name=s_data) | 
                Q(worker__username__icontains=s_data) | 
                Q(creator__username__icontains=s_data) | 
                Q(task__icontains=s_data) | 
                Q(status__icontains=s_data))).order_by('-created_date'), 40)
            
        return render(request, 'logs/tasks_log_page.html', context={
            'logs': logs.get_page(page_number),
            'tasks': tasks.get_page(page_number)
        })
    else:

        logs = Paginator(
            LogTasks.objects.filter(user__corporation=request.user.corporation).order_by('-date'),
            40)
        
        tasks = Paginator(
            Tasks.objects.filter(company=request.user.corporation, active=True).order_by('-created_date'),
            40)

        return render(request, 'logs/tasks_log_page.html', context={
            'logs': logs.get_page(page_number),
            'tasks': tasks.get_page(page_number)
        })
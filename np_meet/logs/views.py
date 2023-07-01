from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def index_log_page(request):
    s_data = request.GET.get('q')
    if s_data:
        
        logs = LogsInvites.objects.filter(Q(company=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(creator__username=s_data) | 
            Q(code=s_data) |
            Q(do=s_data))).order_by('-created_date')
        
        logs.union(LogAuthUser.objects.filter(Q(user__corporation=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(user__username=s_data) | 
            Q(do=s_data))).order_by('-date_login'))
            
        return render(request, 'logs/invites_log_page.html', context={
            'logs': logs
        })
    else:
        logs = LogsInvites.objects.filter(company=request.user.corporation).order_by('-created_date')
        logs.union(LogAuthUser.objects.filter(user__corporation=request.user.corporation).order_by('-date_login'))
        return render(request, 'logs/invites_log_page.html', context={
            'logs': logs
        })

@login_required
def invites_log_page(request):
    s_data = request.GET.get('q')
    if s_data:
        
        logs = LogsInvites.objects.filter(Q(company=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(creator__username=s_data) | 
            Q(code=s_data) |
            Q(do=s_data))).order_by('-created_date')
            
        return render(request, 'logs/invites_log_page.html', context={
            'logs': logs
        })
    else:
        logs = LogsInvites.objects.filter(company=request.user.corporation).order_by('-created_date')
        return render(request, 'logs/invites_log_page.html', context={
            'logs': logs
        })

@login_required
def auth_log_page(request):
    s_data = request.GET.get('q')
    if s_data:
        
        logs = LogAuthUser.objects.filter(Q(user__corporation=request.user.corporation) & (
            Q(company__name=s_data) | 
            Q(user__username=s_data) | 
            Q(do=s_data))).order_by('-date_login')
            
        return render(request, 'logs/auth_log_page.html', context={
            'logs': logs
        })
    else:
        logs = LogAuthUser.objects.filter(user__corporation=request.user.corporation).order_by('-date_login')
        return render(request, 'logs/auth_log_page.html', context={
            'logs': logs
        })
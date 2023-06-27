from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(LogsInvites)
class LogsInvitesChanch(admin.ModelAdmin):
    list_display = ('id', 'company', 'creator', 'code', 'do', 'created_date')
    list_display_links = ('id',)
    list_filter = ('do', 'created_date')
    
    readonly_fields = ('id', 'company', 'creator', 'code', 'do', 'created_date')
    search_fields = ('id', 'company__name', 'creator__username', 'code', 'do', 'created_date')


@admin.register(LogAuthUser)
class LogAuthUserChanch(admin.ModelAdmin):
    list_display = ('id', 'user', 'do', 'date_login', 'company')
    list_display_links = ('id',)
    list_filter = ('do', 'date_login')
    readonly_fields = ('id', 'user', 'do', 'date_login', 'company')
    search_fields = ('id', 'user__username', 'do', 'date_login')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "avatar")}),
        (_("Personal info"), 
            {"fields": (
                "first_name", 
                "last_name",
                "birth_date", 
                "email", 
                "phone",
                'corporation', 
                "position",
                'reg_ip',
                'last_ip'
                )
            }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "first_name", "last_name", 'birth_date', "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", 'birth_date')
    search_fields = ("username", "first_name", "last_name", "email", 'birth_date')
    # list_editable = ('is_staff',)
    readonly_fields = ('reg_ip', 'last_ip')

@admin.register(CompInvites)
class CompInvites(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'company',
                'code'
            ),

        }),
        (_('Настройки'), {
            'fields': (
                'creator',
                'activations',
                'max_activations',
                'is_active',
            )
        }),
        (_('Важные даты'), {
            'fields': (
                'created_date',
                'last_invite'
            )
        })
    )
    list_display = ('company', 'code', 'creator', 'activations', 'max_activations', 'is_active')
    list_display_links = ('company', 'code', 'creator', 'activations', 'max_activations')
    list_editable = ('is_active',)
    search_fields = ('company__name', 'code', 'creator__username', 'activations', 'max_activations')
    list_filter = ('company', 'activations', 'max_activations', 'is_active')
    readonly_fields = ('created_date', 'last_invite')




admin.site.register(Corporations)
admin.site.register(UserPermisions)
admin.site.register(CorpPositions)
# admin.site.register(User)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_log_page, name='index_log_page'),
    path('invites/', views.invites_log_page, name='invites_log_page'),
    path('auth/', views.auth_log_page, name='auth_log_page'),
    path('tasks/', views.tasks_log_page, name='tasks_log_page'),
]


from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index_page, name='home_page'),
    path('singup/', views.singup_user_page, name='singupuser_page'),
    path('login/', views.login_user_page, name='login_user_page'),
    path('logout/', views.logoutuser, name='logout_user'),
    path('controlpanel/', views.control_palen_page, name='control_palen_page'),
    path('company/create/', views.create_comp_page, name='create_comp_page'),
    path('company/profile/<int:comp_id>/', views.company_profile_page, name='company_profil_page'),
    path('company/workers/profile/<int:user_id>/fire/>', views.fire_worker, name='fire_worker'),
    path('company/workers/profile/<int:user_id>', views.profile_page, name='profile_page'),
    path('company/workers/invites/delete/<int:invite_id>', views.delete_worker_invite, name='delete_worker_invite'),
    path('company/workers/invites/create', views.create_worker_invite, name='create_worker_invite'),
    path('company/workers/invites/join', views.join_worker_invite, name='join_worker_invite'),
    path('company/workers/', views.company_workers_page, name='company_workers_page')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

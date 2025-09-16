from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    # path('auth/logout/', views.logout, name='logout'),
    # path('auth/refresh/', views.logout, name='refresh'),
    # path('profile', views.profile, name='profile'),
]
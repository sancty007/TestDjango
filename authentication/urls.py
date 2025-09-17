from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/forgotPassword', views.ForgotPassword, name='ForgotPassword'),
    path('auth/changePassword/<int:id>', views.changePassword, name='changePassword'), 
    # path('auth/refresh/', views.logout, name='refresh'),
    # path('profile', views.profile, name='profile'),
]
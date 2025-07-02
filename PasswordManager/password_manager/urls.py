from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('password-entry/create/', views.create_password_entry, name='create_password_entry'),
    path('password-entry/<int:pk>/update/', views.update_password_entry, name='update_password_entry'),
    path('password-entry/<int:pk>/delete/', views.delete_password_entry, name='delete_password_entry'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('dashboard/', views.dashboard_view),
    path('enter/', views.enter_password_view),
    path('access/', views.view_passwords_view),
    path('delete/<int:id>/', views.delete_password_view, name='delete_password'),
]

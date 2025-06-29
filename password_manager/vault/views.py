from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import PasswordEntry
from django.shortcuts import get_object_or_404



def home_view(request):
    return render(request, 'home.html')



def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('/login/')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def enter_password_view(request):
    if request.method == "POST":
        title = request.POST['title']
        password = request.POST['password']
        PasswordEntry.objects.create(user=request.user, title=title, password=password)
        return redirect('/dashboard/')
    return render(request, 'enter_password.html')

@login_required
def view_passwords_view(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'view_passwords.html', {'passwords': passwords})

@login_required
def delete_password_view(request, id):
    password_entry = get_object_or_404(PasswordEntry, id=id, user=request.user)
    password_entry.delete()
    return redirect('/access/')
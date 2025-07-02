# password_manager/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, OTPForm, ResetPasswordForm, PasswordEntryForm
from .models import PasswordEntry, PasswordResetOTP
from django.contrib.auth.models import User  # Add this import
import random
import string
from datetime import timedelta

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            next_url = request.POST.get('next', '')
            if not next_url:
                next_url = reverse('dashboard')
            try:
                return redirect(next_url)
            except NoReverseMatch as e:
                print(f"Reverse error: {e}")
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    next_param = request.GET.get('next', '')
    return render(request, 'registration/login.html', {'form': form, 'next': next_param})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = ''.join(random.choices(string.digits, k=6))
                expires_at = timezone.now() + timedelta(minutes=10)
                PasswordResetOTP.objects.create(user=user, otp=otp, expires_at=expires_at)
                try:
                    send_mail(
                        subject='Password Reset OTP',
                        message=f'Your OTP is {otp}. It is valid for 10 minutes.',
                        from_email='from@example.com',  # Arbitrary for console backend
                        recipient_list=[email],
                        fail_silently=False,
                    )         
                    print(f"OTP {otp} sent to {email}")  # Debug output
                    messages.success(request, 'OTP sent to your email. Check the console for the OTP.')
                    return redirect('verify_otp')
                except Exception as e:
                    print(f"Email sending failed: {e}")  # Debug email errors
                    messages.error(request, 'Failed to send OTP. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email.')
        else:
            messages.error(request, 'Invalid email format.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgot_password.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                otp_entry = PasswordResetOTP.objects.get(otp=otp, expires_at__gt=timezone.now())
                request.session['reset_user_id'] = otp_entry.user.id
                return redirect('reset_password')
            except PasswordResetOTP.DoesNotExist:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPForm()
    return render(request, 'registration/verify_otp.html', {'form': form})

def reset_password(request):
    if 'reset_user_id' not in request.session:
        return redirect('forgot_password')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.session['reset_user_id'])
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            PasswordResetOTP.objects.filter(user=user).delete()
            del request.session['reset_user_id']
            messages.success(request, 'Password reset successful. Please log in.')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'registration/reset_password.html', {'form': form})

@login_required
def dashboard(request):
    entries = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'entries': entries})

@login_required
def create_password_entry(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Password entry created successfully.')
            return redirect('dashboard')
    else:
        form = PasswordEntryForm()
    return render(request, 'password_entry_form.html', {'form': form})

@login_required
def update_password_entry(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password entry updated successfully.')
            return redirect('dashboard')
    else:
        form = PasswordEntryForm(instance=entry)
    return render(request, 'password_entry_form.html', {'form': form})

@login_required
def delete_password_entry(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Password entry deleted successfully.')
        return redirect('dashboard')
    return render(request, 'password_entry_detail.html', {'entry': entry})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

def home(request):
    return render(request, 'home.html')
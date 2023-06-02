from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAuthenticationFormForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.


# 테스트용 index입니다
def index(request):
    return render(request, 'accounts/index.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('studies:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend',)
            # return redirect('studies:index')  # 임시 index
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('studies:index')
    
    if request.method == 'POST':
        form = CustomAuthenticationFormForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # return redirect('studies:index')  # 임시 index
            return redirect('main')
    else:
        form = CustomAuthenticationFormForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    # return redirect('studies:index')  # 임시 index
    return redirect('main')


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    # return redirect('studies:index')  # 임시 index
    return redirect('main')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # return redirect('studies:index')  # 임시 index
            return redirect('main')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # return redirect('studies:index')  # 임시 index
            return redirect('main')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    user = get_user_model()
    person = user.objects.get(username=username)
    context = {
        'person': person
    }
    return render(request, 'accounts/profile.html', context)
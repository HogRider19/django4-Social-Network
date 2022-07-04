from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'account/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'account/signup.html', {'form':UserCreationForm(), 'error' : 'Такое имя пользователя уже занято'})
        else:
            return render(request, 'account/signup.html', {'form':UserCreationForm(), 'error' : 'Введенные пароли не совадают'})



def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('dashboard')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'account/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password'],
        )

        if user is None:
            return render(request, 'account/login.html', {'form':AuthenticationForm(), 'error':'Неправельный логин или пароль'})
        else:
            login(request, user)
            return redirect('dashboard')

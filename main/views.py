from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from main.models import Account


# VIEWS
def loginView(request):
    return render(request, 'login.html')


def signupView(request):
    return render(request, 'signup.html')


def dashView(request):
    if request.user.is_authenticated:
        context = {
            "username": request.user.username,
            "userImg": request.user.user_img
        }

        return render(request, 'dash.html', context=context)
    else:
        return redirect('loginView')


# PROCESS
def processLogin(request):
    email, username, password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password')
    user = authenticate(email=email, username=username, password=password)
    if user is not None:
        return redirect('dashView')
    else:
        return redirect('loginView')


def processSignup(request):
    email, username, password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password')
    user = Account.objects.create_user(email=email, username=username, password=password)
    login(request, user)
    return redirect('dashView')

from django.shortcuts import render, redirect
from main.models import Account


# VIEWS
def loginView(request):
    return render(request, 'login.html')


def signupView(request):
    return render(request, 'signup.html')


def dashView(request):
    return render(request, 'dash.html')


# PROCESS
def processLogin(request):
    email, username, password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password')
    return render(request, 'signup.html')


def processSignup(request):
    email, username, password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password')
    user = Account.objects.create_user(email=email, username=username, password=password)

    return redirect('dashView')

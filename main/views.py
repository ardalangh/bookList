import urllib

import requests
from django.contrib.auth import authenticate, login, logout
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
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0:2].upper(),
            "books": [
                {
                    "id": book.id,
                    "name": book.name,
                    "bookImgUrl": book.imgUrl
                } for book in request.user.books.all()
            ]
        }

        return render(request, 'dash.html', context=context)
    else:
        return redirect('loginView')


def searchResultView(request):
    return render(request, "searchResult.html", {'bookQueries': request.session['lastSearch']})


# PROCESS
def processLogin(request):
    email, username, password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password')
    user = authenticate(email=email, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('dashView')
    else:
        return redirect('loginView')


def processSignup(request):
    email, username, password = request.POST.get('email'), request.POST.get('username'), request.POST.get('password')
    user = Account.objects.create_user(email=email, username=username, password=password)
    login(request, user)
    return redirect('dashView')


def processLogout(request):
    logout(request)
    return redirect('loginView')


def processBookSearch(request):
    if request.method == 'GET':
        bookNameToBeSearched = request.GET.get('bookName')
        api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"
        google_host = "https://www.googleapis.com/books/v1/volumes"
        f = {'q': bookNameToBeSearched, 'key': api_key}
        google_host += "?" + urllib.parse.urlencode(f)
        res = requests.get(google_host).json()
        request.session['lastSearch'] = res
        return redirect('searchResultView')

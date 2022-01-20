import urllib
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
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
    bookName = request.GET.get('bookName')
    requestResponse = getResFromGoogle(bookName)
    request.session["lastSearchData"] = requestResponse

    if request.method == 'GET' and bookName:
        context = {
            **requestResponse,
            "username": request.user.username,
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0:2].upper(),
        }
        return render(request, "searchResult.html", context=context)


def bookInfoView(request, id):
    targetBook = list(filter(lambda b: b["id"] == id, request.session["lastSearchData"]["items"]))
    if len(targetBook) > 0:
        context = {
            **targetBook[0],
            "username": request.user.username,
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0:2].upper(),
        }
        return render(request, 'bookInfo.html', context=context)


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
    if not email or not username or not password:
        messages.error(request, 'Please provide all the required fields: username, email, password')
        return redirect('signupView')
    try:
        user = Account.objects.create_user(email=email, username=username, password=password)
        login(request, user)
        return redirect('dashView')
    except IntegrityError:
        messages.error(request, 'Username or email must is already registered')
        return redirect('signupView')


def processLogout(request):
    logout(request)
    return redirect('loginView')


# HELPER
def getResFromGoogle(bookName):
    api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"
    google_host = "https://www.googleapis.com/books/v1/volumes"
    f = {'q': bookName, 'key': api_key}
    google_host += "?" + urllib.parse.urlencode(f)
    return requests.get(google_host).json()

# def getResFromGoogleById(id):
#     api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"
#     google_host = "https://books.google.com/bbooks/v1/volumes"
#     f = {'id': id, 'key': api_key}
#     google_host += "?" + urllib.parse.urlencode(f)
#     return requests.get(google_host).json()

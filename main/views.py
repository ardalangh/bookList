import random
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
        books = request.user.books

        context = {
            "username": request.user.username,
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0].upper(),
            "userRandomColor": request.user.userRandomColor,
            "books": [
                {
                    "kind": "backendTrimmed",
                    "id": bookId,
                    "name": books[bookId]["volumeInfo"]["title"],
                    "bookImgUrl": books[bookId]["volumeInfo"]["imageLinks"]["thumbnail"],
                    "shortDescription": books[bookId]["volumeInfo"]["description"][0:100] + "...",
                } for bookId in books.keys()
            ]
        }

        if "lastSearchData" in request.session:
            request.session["lastSearchData"].extend(context["books"])
        else:
            request.session["lastSearchData"] = context["books"]


        return render(request, 'dash.html', context=context)
    else:
        return redirect('loginView')


def searchResultView(request):
    bookName = request.GET.get('bookName')
    requestResponse = getResFromGoogle(bookName)
    if request.method == 'GET' and bookName:
        request.session["lastSearchData"] = getItemsFromGoogleResponse(requestResponse)
        context = {
            **requestResponse,
            "username": request.user.username,
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0].upper(),
        }
    else:
        context = {
            **request.session["lastSearchData"],
            "username": request.user.username,
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0:2].upper(),
        }
    return render(request, "searchResult.html", context=context)


def bookInfoView(request, id):

    targetBook = list(filter(lambda b: b["id"] == id, request.session["lastSearchData"]))
    targetBook = getResFromGoogleById(id)

    print(targetBook["volumeInfo"])


    if len(targetBook) > 0:
        context = {
            **targetBook["volumeInfo"],
            "username": request.user.username,
            "userImg": request.user.user_img,
            "userInitial": request.user.username[0].upper(),
        }
        return render(request, 'bookInfo.html', context=context)


# PROCESS
def processLogin(request):
    username, password = request.POST.get('username'), request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('dashView')
    else:
        messages.error(request, "Your credentials are invalid please try again")
        return redirect('loginView')


def processSignup(request):
    """ processes for the signup end point """
    # retrieve authentication data from front-end
    username, password = request.POST.get('username'), request.POST.get('password')
    # if username and password is not inputted redirect to the sign up page and display and error message
    if not username or not password:
        messages.error(request, 'Please provide all the required fields: username, password')
        return redirect('signupView')
    # tries to create a new user with the inputted data
    try:
        # create a user with the given cred data
        user = Account.objects.create_user(
            username=username,
            password=password,
        )
        # generate a new random color for the user and save it in the db
        user.userRandomColor = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0]
        user.save()
        # login the user so we can access request.user in many HTTP requests and redirect to dash page
        login(request, user)
        return redirect('dashView')
    # if username exists redirect back to the sign up page and display an error
    except IntegrityError:
        messages.error(request, 'Username is already registered')
        return redirect('signupView')


def processLogout(request):
    """ processes for the logout end point """
    # log the user out and redirect to the login page
    logout(request)
    return redirect('loginView')


def processAddToReadingList(request):
    bookId = request.POST.get('bookId')
    bookData = list(filter(lambda b: b["id"] == bookId, request.session["lastSearchData"]))

    if bookId not in request.user.books and len(bookData) > 0:
        request.user.books[bookId] = bookData[0]
        request.user.save()
        return redirect('dashView')
    else:
        messages.error(request, f"Book id {bookId} is already in your list")
        return redirect('searchResultView')


def processDeleteFromReadingList(request, id):
    if id in request.user.books:
        del request.user.books[id]
        request.user.save()
    else:
        messages.error(request, f"book if {id} is not in your reading list")

    return redirect('dashView')


# HELPER

def getResFromGoogleById(id):
    api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"
    google_host = f"https://www.googleapis.com/books/v1/volumes/{id}?key={api_key}"
    return requests.get(google_host).json()


def getResFromGoogle(bookName):
    api_key = "AIzaSyDzp_LKa5V2u5vtPu1cMtTKM287r7KW50s"
    google_host = "https://www.googleapis.com/books/v1/volumes"
    f = {'q': bookName, 'key': api_key}
    google_host += "?" + urllib.parse.urlencode(f)
    return requests.get(google_host).json()


def getItemsFromGoogleResponse(data):
    return data["items"] if "items" in data else []

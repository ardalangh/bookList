import random
import urllib
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from main.models import Account


# VIEWS
def loginView(request):
    return render(request, 'login.html')


def signupView(request):
    return render(request, 'signup.html')


@login_required
def dashView(request):
    books = request.user.books
    context = {
        **generateUserRelatedContext(request.user),
        "books": [
            {
                "kind": "backendTrimmed",
                "id": bookId,
                "name": books[bookId]["volumeInfo"]["title"],
                "safeName": books[bookId]["volumeInfo"]["title"][0:32],
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


@login_required
def searchResultView(request):
    bookName = request.GET.get('bookName')
    requestResponse = getResFromGoogle(bookName)
    items = getItemsFromGoogleResponse(requestResponse)

    googleRes = [{**book, "safeTitle": f"{book['volumeInfo']['title'][0:32]}."} for book in items]
    if request.method == 'GET' and bookName:
        request.session["lastSearchData"] = getItemsFromGoogleResponse(requestResponse)
        context = {
            "items": googleRes,
            **generateUserRelatedContext(request.user)
        }
    else:
        context = {
            "items": googleRes,
            **generateUserRelatedContext(request.user)
        }
    return render(request, "searchResult.html", context=context)


@login_required
def bookInfoView(request, id):
    targetBook = getResFromGoogleById(id)
    if len(targetBook) > 0:
        context = {
            **targetBook["volumeInfo"],
            **generateUserRelatedContext(request.user)
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
    bookData = getResFromGoogleById(bookId)
    if bookId not in request.user.books and "volumeInfo" in bookData:
        request.user.books[bookId] = bookData
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


def processUserImgUpload(request):
    if request.method == 'POST':
        uploadedImage = request.FILES.get("data")
        request.user.user_img = uploadedImage
        request.user.save()
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


def generateUserRelatedContext(user) -> dict:
    """
    <django.utils.functional.SimpleLazyObject>    user : the authenticated instance of request.user
    <dict> Returns: a dictionary with all the user related context that needs to be send back to frontend
    """
    return {
        "username": user.username,
        "userImg": user.user_img,
        "userInitial": user.username[0].upper(),
        "userRandomColor": user.userRandomColor,
    }


def getItemsFromGoogleResponse(data):
    return data["items"] if "items" in data else []

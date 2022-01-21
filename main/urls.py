from django.urls import path
from main.views import loginView, signupView, processLogin, processSignup, dashView, processLogout, \
    searchResultView, bookInfoView, processAddToReadingList, processDeleteFromReadingList

urlpatterns = [
    path('', loginView, name='loginView'),
    path('signup/', signupView, name='signupView'),
    path('dash/', dashView, name='dashView'),
    path('searchResultView/', searchResultView, name='searchResultView'),
    path('bookInfoView/<slug:id>/', bookInfoView, name='bookInfoView'),

    path('processLogin/', processLogin, name='processLogin'),
    path('processSignup/', processSignup, name='processSignup'),
    path('processLogout/', processLogout, name='processLogout'),


    path('processAddToReadingList/', processAddToReadingList, name='processAddToReadingList'),
    path('processDeleteFromReadingList/<slug:id>/', processDeleteFromReadingList, name='processDeleteFromReadingList'),

]

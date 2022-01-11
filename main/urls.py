from django.urls import path
from main.views import loginView, signupView, processLogin, processSignup, dashView, processLogout

urlpatterns = [
    path('', loginView, name='loginView'),
    path('signup/', signupView, name='signupView'),
    path('dash/', dashView, name='dashView'),




    path('processLogin/', processLogin, name='processLogin'),
    path('processSignup/', processSignup, name='processSignup'),
    path('processLogout/', processLogout, name='processLogout'),
]

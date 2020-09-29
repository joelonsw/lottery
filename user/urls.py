from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('signin/', signin, name="signin"),
    path('mypage/', mypage, name="mypage"),
    path('signup/', signup, name="signup"),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('signin/', signin, name="signin"),
    path('logout/', log_out, name="logout"),
    path('mypage/', mypage, name="mypage"),
    path('signup/', signup, name="signup"),
]
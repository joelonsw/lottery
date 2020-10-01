"""lotterypjt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import lotteryapp.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lotteryapp.views.home, name="home"),
    path('main', lotteryapp.views.main, name="main"),
    path('share', lotteryapp.views.share, name="share"),
    path('request', lotteryapp.views.request, name="request"),
    path('write', lotteryapp.views.write, name="write"),
    path('write_request', lotteryapp.views.write_request, name="write_request"),
    path('write_share', lotteryapp.views.write_share, name="write_share"),
    path('detail', lotteryapp.views.detail, name="detail"),
    path('share_response', lotteryapp.views.share_response, name="share_response"),
    path('request_response', lotteryapp.views.request_response, name="request_response"),
    # My page 관련 추가된 부분.
    path('mypage/<str:id>/', user.views.mypage, name="mypage"),
    path('mypage/<str:id>/request/<int:pk>', user.views.mypage_detail, name="mypage_detail"),
]

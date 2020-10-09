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
from django.urls import path, include
import lotteryapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main', lotteryapp.views.main, name="main"),
    path('share', lotteryapp.views.share, name="share"),
    path('request', lotteryapp.views.request, name="request"),
    path('write', lotteryapp.views.write, name="write"),
    path('write_request', lotteryapp.views.write_request, name="write_request"),
    path('write_share', lotteryapp.views.write_share, name="write_share"),
    #detail과 share_response, request_response를 합쳐 두개로 나눴습니다 1.share_detail 2.request_detail 
    path('share_detail/<int:detail_id>', lotteryapp.views.share_detail, name="share_detail"),
    path('request_detail/<int:detail_id>', lotteryapp.views.request_detail, name="request_detail"),    
    path('share_accept/<int:detail_id>', lotteryapp.views.share_accept, name="share_accept"),
    path('request_accept/<int:detail_id>', lotteryapp.views.request_accept, name="request_accept"),
    #about.html 추가 -> 여기엔 우리 팀정보
    path('about', lotteryapp.views.about, name="about"),
    path('', include('user.urls')),
]

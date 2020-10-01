from django.shortcuts import render
from user.models import User
from lotteryapp.models import DummyRequest, DummyShare
from django.http import Http404

# Create your views here.

def mypage(request, id):
    # 전체 임시 user instance 중에서 현재 유저를 가져옴
    now_user = User.objects.get(user_id=id)
    # DB 내 전체 request instance 중에서 현재 유저를 foreign key로 가지는 instance를 필터링
    request_list = DummyRequest.objects.filter(author_id=now_user)
    return render(request, "mypage.html", {'user' : now_user, 'requests' : request_list})


def mypage_detail(request, id, pk):
    now_user = User.objects.get(user_id=id)
    request_target = DummyRequest.objects.get(author_id=now_user, pk_num=pk)
    return render(request, "test_detail.html", {'request_target' : request_target})
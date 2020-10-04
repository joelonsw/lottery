from django.db import models
from django.conf import settings
from user.models import Profile

# Create your models here.

# model을 만들때 Share/Request 모델을 각각, 혹은 퉁쳐서 만들면 될듯

# model에 필요한 것들 
# ----------------------------------------
# 성격 : Share(나눠드립니다) or Request(부족합니다)
# 게시자 : User를 ForeignKey로 연결
# 위치 : 점포의 위치 정보(user의 점포가 default)
# 품목 : 부족한 품목 or 남는 품목
# 수량 : 부족한 수량 or 남는 수량
# 유효기간 : 만료되는 시간

"""
    Dummy model request/share class 입니다.
    임시로 내용을 모두 text나 integer로 저장하고 로직을 실행할 목적으로 사용합니다.
    이 후 로직이 완성되면 model을 고칠 예정입니다.
"""

"""
    location => 요청 지점
    contents => 본문 내용
    minute   => 만료 시간 (일단 분 단위)
    item     => 필요한 품목 이름
    item_num => 필요한 품목 개수
    dates    => 게시 날짜
    pk_num   => primary key
    author   => 게시한 유저의 foreign key
"""

class DummyRequest(models.Model):

    location    = models.CharField(max_length=100)
    item        = models.CharField(max_length=50)
    item_num    = models.IntegerField(default=0)
    limit_time  = models.TimeField(auto_now=True)
    email       = models.CharField(max_length=100, blank=True)
    phone       = models.CharField(max_length=15, blank=True)
    contents    = models.TextField(max_length=1000)

    dates       = models.DateField(auto_now=True)
    pk_num      = models.AutoField(primary_key=True, auto_created=True)
    author      = models.ForeignKey("user.Profile", on_delete=models.CASCADE)
    outdate     = False

    def __str__ (self):
        return str(self.author)


class DummyShare(models.Model):

    location    = models.CharField(max_length=100)
    item        = models.CharField(max_length=50)
    item_num    = models.IntegerField(default=0)
    limit_time  = models.TimeField(auto_now=True)
    email       = models.CharField(max_length=100, blank=True)
    phone       = models.CharField(max_length=15, blank=True)
    contents    = models.TextField(max_length=1000)
    
    dates       = models.DateField(auto_now=True)
    pk_num      = models.AutoField(primary_key=True, auto_created=True, default=1)
    author      = models.ForeignKey("user.Profile", on_delete=models.CASCADE)
    outdate     = False

    def __str__ (self):
        return self.location

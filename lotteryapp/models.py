from django.db import models
from django.conf import settings
from user.models import *
from datetime import datetime

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
    location    => 요청 지점
    contents    => 본문 내용
    minute      => 만료 시간 (일단 분 단위)
    item        => 필요한 품목 이름
    item_num    => 필요한 품목 개수
    dates       => 게시 날짜
    pk_num      => primary key
    author      => 게시한 유저의 foreign key

    아래 변수는 utils.py에 update_remain이 호출되면 업데이트 되는 변수들 입니다.
    remain      => 요청이나 공유가 들어왔을 때, 들어온 만큼의 수량을 여기서 깎습니다.

    아래 변수는 utils.py에 update_outdate가 호출되면 업데이트 되는 변수들 입니다.
    remain_time => limit_time까지 남은 시간을 초로 환산해서 저장
    outdate     => 시간이 만료되면 이 값을 True로 바꿔줍니다.
"""

class ItemRequest(models.Model):

    location    = models.CharField(max_length=100)
    item        = models.CharField(max_length=50)
    item_num    = models.IntegerField(default=0)
    limit_time  = models.CharField(max_length=100)
    email       = models.CharField(max_length=100, blank=True)
    phone       = models.CharField(max_length=15, blank=True)
    contents    = models.TextField(max_length=1000)

    dates       = models.DateTimeField(auto_now=True)
    pk_num      = models.AutoField(primary_key=True, auto_created=True)
    author      = models.ForeignKey("user.Profile", on_delete=models.CASCADE)

    remain      = models.IntegerField(default=0)
    remain_time = models.IntegerField(default=0)
    outdate     = models.BooleanField(default=False)

    def __str__ (self):
        return str(self.dates)


class ItemShare(models.Model):

    location    = models.CharField(max_length=100)
    item        = models.CharField(max_length=50)
    item_num    = models.IntegerField(default=0)
    limit_time  = models.CharField(max_length=100)
    email       = models.CharField(max_length=100, blank=True)
    phone       = models.CharField(max_length=15, blank=True)
    contents    = models.TextField(max_length=1000)
    
    dates       = models.DateTimeField(auto_now=True)
    pk_num      = models.AutoField(primary_key=True, auto_created=True)
    author      = models.ForeignKey("user.Profile", on_delete=models.CASCADE)

    remain      = models.IntegerField(default=0)
    remain_time = models.IntegerField(default=0)
    outdate     = models.BooleanField(default=False)

    def __str__ (self):
        return str(self.dates)



"""
    request/share detail.html을 보고 그대로 넣었습니다.

    request/share location => 요청/공유를 수락하는 지점
    request/share num      => 요청 또는 공유할 수량
    request/share email    => 요청/공유를 수락하는 사람의 이메일
    request/share phone    => 요청/공유를 수락하는 사람의 번호
    request/share contents => 하고 싶은 말

    volunteer         => 어떤 유저가 요청/공유를 수락하는지 (즉, 댓글 작성자)
    target            => 요청/공유 하고 있는 품목 (즉, 댓글이 달리고 있는 글)
"""

class RequestAccept(models.Model):

    request_location = models.CharField(max_length=100, blank=True)
    request_num      = models.IntegerField(default=0)
    request_email    = models.CharField(max_length=100, blank=True)
    request_phone    = models.CharField(max_length=15, blank=True)
    request_contents = models.TextField(max_length=1000, blank=True)

    target           = models.ForeignKey(ItemRequest, on_delete=models.CASCADE)
    pk_num           = models.AutoField(primary_key=True, auto_created=True)
    volunteer        = models.ForeignKey(User, on_delete=models.CASCADE)
    dates            = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk_num)


class ShareAccept(models.Model):

    share_location   = models.CharField(max_length=100, blank=True)
    share_num        = models.IntegerField(default=0)
    share_email      = models.CharField(max_length=100, blank=True)
    share_phone      = models.CharField(max_length=15, blank=True)
    share_contents   = models.TextField(max_length=1000, blank=True)

    target           = models.ForeignKey(ItemShare, on_delete=models.CASCADE)
    pk_num           = models.AutoField(primary_key=True, auto_created=True)
    volunteer        = models.ForeignKey(User, on_delete=models.CASCADE)
    dates            = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk_num)


"""
    주차별 발주량에 사용할 model 입니다.

    item_name  => 주문한 물건
    item_num   => 주문한 물건의 수량
    order_date => 주문한 날짜
    author     => My Page에서 보여주기 위한 작성자

    따로 모델을 저장하는 페이지가 없으므로 admin에서 넣어주시면 됩니다.
"""
class OrderItem(models.Model):

    item_name  = models.CharField(max_length=100, blank=True)
    item_num   = models.IntegerField(default=0)
    order_date = models.DateField(default=None)
    author     = models.ForeignKey("user.Profile", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item_name)
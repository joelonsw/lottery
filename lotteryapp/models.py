from django.db import models
from django.conf import settings

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

class DummyRequest(models.Model):

    location    = models.CharField(max_length=100)              # 요청 장소
    contents    = models.TextField(blank=True)                  # 본문 내용
    minute      = models.IntegerField(null=True)                # 만료 시간 (일단은 분 단위)
    item        = models.CharField(max_length=50, blank=True)   # 요청 품목 이름
    item_num    = models.IntegerField(null=True)                # 요청 품목 개수
    dates       = models.DateField(auto_now=True)               # 게시 날짜

    def __str__ (self):
        return self.location


class DummyShare(models.Model):

    location    = models.CharField(max_length=100)  # 공유 장소
    contents    = models.TextField(blank=True)      # 본문 내용
    minute      = models.IntegerField()             # 만료 시간 (분 단위)
    item        = models.CharField(max_length=50)   # 공유 품목 이름
    item_num    = models.IntegerField()             # 요청 품목 개수
    dates       = models.DateField(auto_now=True)   # 게시 날짜

    def __str__ (self):
        return self.location
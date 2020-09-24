from django.db import models

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

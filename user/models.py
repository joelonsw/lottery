from django.db import models

# Create your models here.

"""
    임시로 만든 user model 입니다.
"""

"""
    user_id       => 유저 ID
    user_location => 해당 유저의 지점
"""

class User(models.Model):

    user_id = models.CharField(max_length=20)
    user_location = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id
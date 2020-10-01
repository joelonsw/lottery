from django.db import models

# Create your models here.
# 안녕하세요 작업을 다했습니다

class User(models.Model):

    user_id = models.CharField(max_length=20)
    user_location = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id